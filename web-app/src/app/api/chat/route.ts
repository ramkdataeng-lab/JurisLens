import { NextRequest, NextResponse } from "next/server";
import { Message as VercelChatMessage, StreamingTextResponse } from "ai";
import { ChatOpenAI } from "@langchain/openai";
import { AgentExecutor, createOpenAIFunctionsAgent } from "langchain/agents";
import { ChatPromptTemplate, MessagesPlaceholder } from "@langchain/core/prompts";
import { searchRegulationsTool, calculateRiskTool, checkSanctionsTool } from "@/lib/tools";

export const runtime = "nodejs";

const convertVercelMessageToLangChainMessage = (message: VercelChatMessage) => {
    if (message.role === "user") {
        return ["human", message.content];
    } else if (message.role === "assistant") {
        return ["ai", message.content];
    } else {
        return ["human", message.content];
    }
};

export async function POST(req: NextRequest) {
    try {
        const body = await req.json();
        const messages = body.messages ?? [];
        const currentMessageContent = messages[messages.length - 1].content;
        const previousMessages = messages.slice(0, -1).map(convertVercelMessageToLangChainMessage);

        const tools = [searchRegulationsTool, calculateRiskTool, checkSanctionsTool];
        const llm = new ChatOpenAI({
            modelName: "gpt-4-turbo",
            temperature: 0,
            streaming: true,
        });

        const prompt = ChatPromptTemplate.fromMessages([
            ["system", `You are JurisLens, an AI compliance expert. 
      
      1. Use 'search_regulations_tool' to find laws. Provide comprehensive, verbose explanations citing specific articles/sections. 
      2. ALWAYS cite the source document name AND Page Number (if defined) or Section Number (from text) for every claim (e.g., '[Source: file.pdf (Page 5)]' or 'Section 1010.610').
      3. Use 'calculate_risk_tool' for risk assessment and live ledger checks.
      4. Use 'check_sanctions_tool' to verify if individuals or entities are on blacklists or sanctioned watchlists.`],
            ...previousMessages,
            ["human", "{input}"],
            new MessagesPlaceholder("agent_scratchpad"),
        ]);

        const agent = await createOpenAIFunctionsAgent({
            llm,
            tools,
            prompt,
        });

        const agentExecutor = new AgentExecutor({
            agent,
            tools,
        });

        const result = await agentExecutor.invoke({
            input: currentMessageContent,
        });

        return NextResponse.json({ role: "assistant", content: result.output });

    } catch (e: any) {
        console.error(e);
        return NextResponse.json({ error: e.message }, { status: 500 });
    }
}
