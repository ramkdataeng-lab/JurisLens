import { NextRequest, NextResponse } from "next/server";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAIEmbeddings } from "@langchain/openai";
import { ElasticVectorSearch } from "@langchain/community/vectorstores/elasticsearch";
import { Client } from "@elastic/elasticsearch";
import { PDFLoader } from "langchain/document_loaders/fs/pdf";
import { CheerioWebBaseLoader } from "langchain/document_loaders/web/cheerio";
import fs from "fs";
import path from "path";

export const runtime = "nodejs";

export async function POST(req: NextRequest) {
    try {
        const formData = await req.formData();
        const file = formData.get("file") as File | null;
        const url = formData.get("url") as string | null;

        if (!file && !url) {
            return NextResponse.json({ error: "No file or URL provided" }, { status: 400 });
        }

        let documents: import("langchain/document").Document[] = [];


        if (file) {
            const arrayBuffer = await file.arrayBuffer();
            const buffer = Buffer.from(arrayBuffer);
            const tempDir = "/tmp";
            if (!fs.existsSync(tempDir)) {
                fs.mkdirSync(tempDir);
            }
            const tempPath = path.join(tempDir, file.name);

            fs.writeFileSync(tempPath, buffer);

            const loader = new PDFLoader(tempPath);
            documents = await loader.load();

            fs.unlinkSync(tempPath);
        } else if (url) {
            const loader = new CheerioWebBaseLoader(url);
            documents = await loader.load();
        }

        if (!documents || documents.length === 0) {
            return NextResponse.json({ error: "No content found" }, { status: 400 });
        }

        const splitter = new RecursiveCharacterTextSplitter({
            chunkSize: 1000,
            chunkOverlap: 100,
        });

        const docs = await splitter.splitDocuments(documents);

        const elasticCloudId = process.env.ELASTIC_CLOUD_ID;
        const elasticApiKey = process.env.ELASTIC_API_KEY;

        if (!elasticCloudId || !elasticApiKey) {
            return NextResponse.json({ error: "Elasticsearch not configured" }, { status: 500 });
        }

        const client = new Client({
            cloud: { id: elasticCloudId },
            auth: { apiKey: elasticApiKey },
        });

        const embeddings = new OpenAIEmbeddings();
        const vectorStore = new ElasticVectorSearch(embeddings, {
            client,
            indexName: "jurislens_docs",
        });

        await vectorStore.addDocuments(docs);

        return NextResponse.json({ success: true, count: docs.length });

    } catch (e: any) {
        console.error(e);
        return NextResponse.json({ error: e.message }, { status: 500 });
    }
}
