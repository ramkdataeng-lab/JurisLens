import { NextRequest, NextResponse } from "next/server";
import { RecursiveCharacterTextSplitter } from "langchain/text_splitter";
import { OpenAIEmbeddings } from "@langchain/openai";
import { ElasticVectorSearch } from "@langchain/community/vectorstores/elasticsearch";
import { Client } from "@elastic/elasticsearch";
import { PDFLoader } from "langchain/document_loaders/fs/pdf";
import { CheerioWebBaseLoader } from "langchain/document_loaders/web/cheerio";
import fs from "fs";
import path from "path";
import os from "os";

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

            // Use OS-specific temp directory
            const tempDir = os.tmpdir();
            const tempPath = path.join(tempDir, `jurislens_${Date.now()}_${file.name}`);

            fs.writeFileSync(tempPath, buffer);

            try {
                // PDFLoader in web/Node environments needs to be configured or pdf-parse must be present
                const loader = new PDFLoader(tempPath, {
                    splitPages: true,
                });
                documents = await loader.load();
            } finally {
                // Always clean up temp file
                if (fs.existsSync(tempPath)) {
                    fs.unlinkSync(tempPath);
                }
            }
        } else if (url) {
            const loader = new CheerioWebBaseLoader(url);
            documents = await loader.load();
        }

        if (!documents || documents.length === 0) {
            console.error("❌ No documents were loaded from the source.");
            return NextResponse.json({ error: "No content could be extracted from this document." }, { status: 400 });
        }

        const splitter = new RecursiveCharacterTextSplitter({
            chunkSize: 1000,
            chunkOverlap: 100,
            separators: ["\n\n", "\n", " ", ""],
        });

        // Ensure every doc has a source and page in metadata for Citations
        const sourceName = file ? file.name : (url || "Web Source");
        const docs = (await splitter.splitDocuments(documents)).map((doc, idx) => {
            return {
                ...doc,
                metadata: {
                    ...doc.metadata,
                    source: sourceName,
                    chunk_id: idx,
                    ingested_at: new Date().toISOString()
                }
            };
        });

        const elasticCloudId = process.env.ELASTIC_CLOUD_ID;
        const elasticApiKey = process.env.ELASTIC_API_KEY;

        if (!elasticCloudId || !elasticApiKey) {
            console.error("❌ Elasticsearch environment variables are missing.");
            return NextResponse.json({ error: "Vercel Environment Variables (ELASTIC_CLOUD_ID/API_KEY) are missing." }, { status: 500 });
        }

        try {
            const client = new Client({
                cloud: { id: elasticCloudId },
                auth: { apiKey: elasticApiKey },
            });

            // Index the documents
            console.log(`📦 Indexing ${docs.length} semantic chunks to Elasticsearch index 'jurislens_docs'...`);

            // Handle indexing manually to ensure we see errors
            for (const doc of docs) {
                await client.index({
                    index: "jurislens_docs",
                    document: {
                        content: doc.pageContent,
                        metadata: doc.metadata,
                        text: doc.pageContent, // Fallback field
                        "ml.tokens": {} // Placeholder for ELSER compatibility if needed later
                    }
                });
            }

            console.log("✅ Indexing Complete!");
            return NextResponse.json({ success: true, count: docs.length, source: sourceName });

        } catch (esError: any) {
            console.error("❌ Elasticsearch Indexing Error:", esError);
            return NextResponse.json({ error: `Elasticsearch Error: ${esError.message}` }, { status: 500 });
        }

    } catch (e: any) {
        console.error("❌ Critical Ingestion Failure:", e);
        return NextResponse.json({ error: e.message || "Unknown server error during ingestion." }, { status: 500 });
    }
}
