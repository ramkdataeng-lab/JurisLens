import { DynamicStructuredTool } from "@langchain/core/tools";
import { z } from "zod";
import { Client } from "@elastic/elasticsearch";
import { ElasticsearchStore } from "@langchain/community/vectorstores/elasticsearch";
import { OpenAIEmbeddings } from "@langchain/openai";

// --- Tool 1: Regulation Search ---
export const searchRegulationsTool = new DynamicStructuredTool({
    name: "search_regulations_tool",
    description: "Useful for finding specific laws, statutes, and compliance regulations from the knowledge base.",
    schema: z.object({
        query: z.string().describe("The search query or question to find relevant regulations for."),
    }),
    func: async ({ query }) => {
        try {
            const elasticCloudId = process.env.ELASTIC_CLOUD_ID;
            const elasticApiKey = process.env.ELASTIC_API_KEY;

            if (!elasticCloudId || !elasticApiKey) {
                return "Elasticsearch not configured. Cannot search regulations.";
            }

            const client = new Client({
                cloud: { id: elasticCloudId },
                auth: { apiKey: elasticApiKey },
            });

            const embeddings = new OpenAIEmbeddings();
            const vectorStore = new ElasticsearchStore(embeddings, {
                client,
                indexName: "jurislens_docs",
            });

            const results = await vectorStore.similaritySearchWithScore(query, 3);

            if (!results || results.length === 0) {
                return "No relevant regulations found.";
            }

            return results.map(([doc, score]) => {
                const source = doc.metadata.source || "Unknown";
                const page = doc.metadata.page ? ` (Page ${parseInt(doc.metadata.page) + 1})` : "";
                return `[Source: ${source}${page}] [Relevance: ${score.toFixed(4)}]\n${doc.pageContent}`;
            }).join("\n\n");

        } catch (error) {
            console.error("Elastic Search Failed:", error);
            return "Error searching regulations.";
        }
    },
});

// --- Tool 2: Risk Calculator ---
export const calculateRiskTool = new DynamicStructuredTool({
    name: "calculate_risk_tool",
    description: "Checks the transaction against the Live Ledger and calculates compliance risk.",
    schema: z.object({
        amount: z.number().describe("The transaction amount."),
        jurisdiction: z.string().describe("The receiving country (e.g. 'Zylaria')."),
    }),
    func: async ({ amount, jurisdiction }) => {
        console.log(`🔌 Connecting to Ledger for ${jurisdiction}...`);
        await new Promise((resolve) => setTimeout(resolve, 1000));

        let priorTransfers = 0;
        if (jurisdiction.toUpperCase().includes("ZYLARIA")) {
            priorTransfers = 2500.00;
            console.log(`⚠️ Found prior transaction: $${priorTransfers}`);
        }

        const totalExposure = amount + priorTransfers;
        const limit = 5000;
        const sanctioned = ["NORTH KOREA", "IRAN", "SYRIA", "RUSSIA"];

        if (sanctioned.includes(jurisdiction.toUpperCase())) {
            return "Risk Level: CRITICAL. Sanctioned Jurisdiction. Blocked immediately.";
        }

        if (totalExposure > limit) {
            return `Risk Level: HIGH. TRANSGRESSION: Daily Aggregate Limit Exceeded.\n` +
                `Current Request: $${amount.toFixed(2)}\n` +
                `Prior Today: $${priorTransfers.toFixed(2)}\n` +
                `Total exposure: $${totalExposure.toFixed(2)} (Limit: $${limit.toFixed(2)})`;
        }

        return `Risk Level: LOW. Safe. Total daily exposure $${totalExposure.toFixed(2)} is within limit ($${limit.toFixed(2)}).`;
    },
});

// --- Tool 3: Sanctions Checker ---
export const checkSanctionsTool = new DynamicStructuredTool({
    name: "check_sanctions_tool",
    description: "Checks if a person or entity is on global sanctions lists.",
    schema: z.object({
        name: z.string().describe("The name of the person or entity to check."),
    }),
    func: async ({ name }) => {
        console.log(`🕵️‍♀️ Scanning Sanctions for: '${name}'...`);
        await new Promise((resolve) => setTimeout(resolve, 1200));

        const sanctionedDb: Record<string, { list: string; id: string; reason: string }> = {
            "IVAN DRAGO": { list: "OFAC SDN", id: "RU-8821", reason: "Connection to prohibited energy sector" },
            "VICTOR KRUM": { list: "EU Watchlist", id: "BG-9910", reason: "High-risk politically exposed person" },
            "LE CHIFFRE": { list: "Interpol Red", id: "FR-007", reason: "Terrorist financing" },
            "GOLIATH BANK": { list: "Internal Blacklist", id: "INT-001", reason: "Conflict of interest" }
        };

        const nameUpper = name.trim().toUpperCase();
        if (sanctionedDb[nameUpper]) {
            const record = sanctionedDb[nameUpper];
            return `🚨 MATCH FOUND: '${name}' is a Sanctioned Entity.\n` +
                `Source: ${record.list}\n` +
                `ID: ${record.id}\n` +
                `Reason: ${record.reason}\n` +
                `Action: IMMEDIATE FREEZE required.`;
        }

        return `✅ CLEAR. No matches found for '${name}' in global sanctions lists.`;
    },
});
