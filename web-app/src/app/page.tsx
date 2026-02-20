"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";

type Message = { role: "user" | "assistant"; content: string };

export default function JurisLensApp() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Hello! I am **JurisLens**. I am your autonomous compliance guardian powered by **Elasticsearch**.\n\n**🎬 Recording Demo Flow:**\n1. **Rule Verification:** *"What is the transfer limit for Zylaria under Project Chimera?"*\n2. **State-Aware Compliance:** *"My client wants to send $4,000 to Zylaria. Is this allowed?"*\n3. **Cross-Domain Sanctions:** *"Can we onboard Ivan Drago as a new client?"*\n\n**Setup:** Make sure to ingest \`goliath_bank_internal_policy.pdf\` in the sidebar first!`,
    },
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [agentStatus, setAgentStatus] = useState("");
  const [progress, setProgress] = useState(0);
  const [urlInput, setUrlInput] = useState("");
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState<"idle" | "success" | "error">("idle");
  const [indexedFiles, setIndexedFiles] = useState<string[]>([]);
  const [thumbs, setThumbs] = useState<Record<number, "up" | "down">>({});
  const scrollRef = useRef<HTMLDivElement>(null);
  const fileRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const handleIngest = async () => {
    const file = fileRef.current?.files?.[0];
    if (!file && !urlInput) return;
    setIsIngesting(true);
    setIngestStatus("idle");
    try {
      const formData = new FormData();
      if (file) formData.append("file", file);
      if (urlInput) formData.append("url", urlInput);
      const res = await fetch("/api/ingest", { method: "POST", body: formData });
      if (res.ok) {
        setIngestStatus("success");
        if (file) setIndexedFiles((p) => [...p, file.name]);
        if (urlInput) setIndexedFiles((p) => [...p, urlInput]);
        setUrlInput("");
        if (fileRef.current) fileRef.current.value = "";
      } else throw new Error();
    } catch { setIngestStatus("error"); }
    finally { setIsIngesting(false); }
  };

  const handleSubmit = async (e: React.FormEvent | null, overrideInput?: string) => {
    if (e) e.preventDefault();
    const text = overrideInput ?? input;
    if (!text.trim() || isLoading) return;
    const newMessages: Message[] = [...messages, { role: "user", content: text }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);
    setProgress(0);
    setAgentStatus("🤖 **AI Agent Active.** Analyzing request...");

    // Animate progress
    let prog = 0;
    const ticker = setInterval(() => {
      prog = Math.min(prog + 2, 92);
      setProgress(prog);
    }, 60);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await res.json();
      if (data.content) {
        setMessages((prev) => [...prev, { role: "assistant", content: data.content }]);
      }
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "⚠️ Error connecting to agent." }]);
    } finally {
      clearInterval(ticker);
      setProgress(100);
      setTimeout(() => { setIsLoading(false); setProgress(0); setAgentStatus(""); }, 500);
    }
  };

  const enrichText = (text: string) => {
    const lower = text.toLowerCase();
    if (lower.includes("risk level: high") || lower.includes("denied") || lower.includes("blocked") || lower.includes("transgression"))
      return { prefix: "🔴 📈 HIGH RISK ALERT", color: "text-red-600" };
    if (lower.includes("risk level: low") || lower.includes("safe") || lower.includes("clear"))
      return { prefix: "🟢 📉 LOW RISK ASSESSMENT", color: "text-green-600" };
    if (lower.includes("risk level: medium") || lower.includes("moderate"))
      return { prefix: "🟠 ⚠️ MEDIUM RISK WARNING", color: "text-orange-500" };
    return null;
  };

  const renderContent = (text: string) => {
    // Bold **text**
    return text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
      part.startsWith("**") && part.endsWith("**")
        ? <strong key={i}>{part.slice(2, -2)}</strong>
        : <span key={i}>{part}</span>
    );
  };

  return (
    <div className="flex h-screen bg-[#f8f9fa] font-sans overflow-hidden" style={{ fontFamily: "'Inter', 'Segoe UI', sans-serif" }}>

      {/* ─── LEFT SIDEBAR ─── */}
      <aside className="w-72 bg-white border-r border-gray-200 flex flex-col shadow-sm z-10 flex-shrink-0">
        <div className="p-4 border-b border-gray-100">
          <Image src="/logo.png" alt="JurisLens" width={220} height={60} className="mx-auto" />
        </div>

        <div className="flex-1 overflow-y-auto p-3 space-y-3">
          {/* Elastic RAG Badge */}
          <div className="bg-indigo-50 rounded-lg p-3 border border-indigo-100">
            <p className="text-sm font-bold text-indigo-700">⚡ Elastic RAG</p>
            <p className="text-xs text-indigo-500 mt-0.5">🔍 <strong>Mode:</strong> Hybrid (Vector + Keyword)</p>
          </div>

          {/* Knowledge Base */}
          <div className="border border-gray-200 rounded-lg overflow-hidden">
            <div className="bg-gray-50 px-3 py-2 border-b border-gray-200">
              <p className="text-xs font-bold text-gray-600 uppercase tracking-wide">📚 Knowledge Base</p>
            </div>
            <div className="p-3 space-y-2">
              {indexedFiles.length > 0 ? (
                <div className="text-xs bg-green-50 text-green-700 px-2 py-1 rounded border border-green-200">
                  ✅ KB: {indexedFiles.length} Item(s) Indexed
                </div>
              ) : (
                <p className="text-xs text-gray-400 italic">ℹ️ Knowledge Base Empty</p>
              )}

              <div>
                <p className="text-[11px] text-gray-500 mb-1 font-medium">Upload Regulations (PDF)</p>
                <label className="flex items-center gap-2 p-2 border-2 border-dashed border-gray-300 rounded-lg text-xs text-gray-500 hover:border-indigo-400 hover:text-indigo-500 cursor-pointer transition-colors">
                  📄 <span>{fileRef.current?.files?.[0]?.name ?? "Choose File"}</span>
                  <input ref={fileRef} type="file" accept=".pdf" className="hidden" onChange={() => { }} />
                </label>
              </div>

              <div>
                <p className="text-[11px] text-gray-500 mb-1 font-medium">Or Paste Web Link:</p>
                <input
                  type="text"
                  placeholder="https://www.ecfr.gov/..."
                  className="w-full text-xs border border-gray-300 rounded-md px-2 py-1.5 focus:outline-none focus:ring-2 focus:ring-indigo-400"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                />
              </div>

              <button
                onClick={handleIngest}
                disabled={isIngesting}
                className={cn(
                  "w-full py-2 rounded-lg text-sm font-bold text-white transition-all",
                  isIngesting ? "bg-purple-400" :
                    ingestStatus === "success" ? "bg-green-500" :
                      ingestStatus === "error" ? "bg-red-500" :
                        "bg-gradient-to-r from-[#8b5cf6] to-[#7c3aed] hover:from-[#7c3aed] hover:to-[#6d28d9] shadow-md hover:shadow-lg"
                )}
              >
                {isIngesting ? "⏳ Processing..." : ingestStatus === "success" ? "✅ Indexed!" : ingestStatus === "error" ? "❌ Failed" : "⚡ Process & Index"}
              </button>
            </div>
          </div>

          {/* Clear Chat */}
          <button
            onClick={() => setMessages([messages[0]])}
            className="w-full py-2 text-sm border border-gray-300 rounded-lg text-gray-600 hover:bg-gray-50 hover:border-gray-400 transition-colors"
          >
            🧹 Clear Chat
          </button>
        </div>

        <div className="p-3 border-t border-gray-100">
          <p className="text-[10px] text-gray-400 text-center">© 2026 JurisLens Inc. | Privacy Policy</p>
        </div>
      </aside>

      {/* ─── MAIN AREA (chat + info panel) ─── */}
      <div className="flex-1 flex overflow-hidden">

        {/* ─── CHAT COLUMN (75%) ─── */}
        <main className="flex-1 flex flex-col overflow-hidden">
          {/* Header */}
          <div className="bg-white border-b border-gray-200 px-6 py-3 shadow-sm">
            <h1 className="text-2xl font-bold text-gray-800">⚖️ JurisLens AI</h1>
            <div className="mt-1 bg-blue-50 border border-blue-200 text-blue-700 text-xs rounded-md px-3 py-2">
              ⚡ <strong>Powered by Elasticsearch:</strong> Hybrid Search (Vector + Keyword) across <strong>Millions</strong> of documents.
            </div>
            <p className="text-sm text-gray-500 mt-1 italic">Navigate Global Financial Regulations with Autonomous Precision.</p>
          </div>

          {/* Messages */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto p-4 space-y-3">
            {messages.map((msg, i) => {
              if (msg.role === "user") return (
                <div key={i} className="flex justify-end">
                  <div className="flex items-start gap-2 max-w-[80%] flex-row-reverse">
                    <div className="w-8 h-8 rounded-full bg-gray-200 flex items-center justify-center text-sm flex-shrink-0">👤</div>
                    <div className="bg-white border border-gray-200 rounded-2xl rounded-tr-sm px-4 py-2.5 text-sm shadow-sm text-gray-800 whitespace-pre-wrap">
                      {msg.content}
                    </div>
                  </div>
                </div>
              );
              const enriched = enrichText(msg.content);
              return (
                <div key={i} className="flex flex-col gap-1">
                  <div className="flex items-start gap-2 max-w-[85%]">
                    <Image src="/logo.png" alt="JurisLens" width={32} height={32} className="rounded-full flex-shrink-0 border border-gray-200" />
                    <div className="bg-white border border-gray-200 rounded-2xl rounded-tl-sm px-4 py-2.5 text-sm shadow-sm text-gray-700 whitespace-pre-wrap">
                      {enriched && (
                        <p className={cn("font-bold text-sm mb-2", enriched.color)}>{enriched.prefix}</p>
                      )}
                      {msg.content.split("\n").map((line, li) => (
                        <p key={li} className={cn("leading-relaxed", line.includes("**") ? "" : "")}>
                          {renderContent(line)}
                        </p>
                      ))}
                    </div>
                  </div>
                  {/* Feedback buttons */}
                  {i > 0 && (
                    <div className="flex justify-end gap-1 max-w-[85%] pr-1">
                      <button onClick={() => setThumbs(t => ({ ...t, [i]: "up" }))}
                        className={cn("text-xs px-1.5 py-0.5 rounded", thumbs[i] === "up" ? "bg-green-100 text-green-600" : "text-gray-400 hover:text-green-500")}>
                        👍
                      </button>
                      <button onClick={() => setThumbs(t => ({ ...t, [i]: "down" }))}
                        className={cn("text-xs px-1.5 py-0.5 rounded", thumbs[i] === "down" ? "bg-red-100 text-red-600" : "text-gray-400 hover:text-red-500")}>
                        👎
                      </button>
                    </div>
                  )}
                </div>
              );
            })}

            {/* Loading state */}
            {isLoading && (
              <div className="flex flex-col gap-2 max-w-[85%]">
                <div className="text-xs text-blue-600 font-medium bg-blue-50 px-3 py-2 rounded-lg border border-blue-200">
                  {agentStatus}
                </div>
                <div className="w-full bg-gray-200 rounded-full h-1.5">
                  <div className="bg-purple-600 h-1.5 rounded-full transition-all duration-300" style={{ width: `${progress}%` }} />
                </div>
              </div>
            )}
          </div>

          <hr className="border-gray-200" />
          <p className="px-6 py-1 text-xs font-semibold text-gray-400 uppercase tracking-wide">💬 Ask a Question</p>

          {/* Input */}
          <div className="p-4 bg-white border-t border-gray-200">
            <form onSubmit={handleSubmit} className="flex gap-2">
              <input
                type="text"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                placeholder="Ask a compliance question..."
                className="flex-1 border border-gray-300 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-purple-400 bg-gray-50"
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-gradient-to-r from-[#8b5cf6] to-[#7c3aed] text-white px-4 py-2.5 rounded-xl text-sm font-bold disabled:opacity-50 hover:shadow-lg transition-all"
              >
                ↗
              </button>
            </form>

            {/* Quick prompts */}
            <div className="flex gap-2 mt-2 flex-wrap">
              {["What is the limit for Zylaria?", "Send $4,000 to Zylaria. Is this allowed?", "Can we onboard Ivan Drago?"].map((q) => (
                <button key={q} onClick={() => handleSubmit(null, q)}
                  className="text-[11px] bg-gray-100 hover:bg-purple-50 hover:text-purple-700 border border-gray-200 hover:border-purple-300 rounded-full px-3 py-1 text-gray-500 transition-colors">
                  {q}
                </button>
              ))}
            </div>
          </div>
        </main>

        {/* ─── RIGHT INFO PANEL (25%) ─── */}
        <aside className="w-64 bg-white border-l border-gray-200 flex flex-col overflow-y-auto flex-shrink-0">
          <div className="p-4 space-y-4">

            <div>
              <p className="text-sm font-bold text-gray-700 mb-2">⚡ Engine</p>
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 text-xs text-blue-800 space-y-1">
                <p>🔍 <strong>Search:</strong> Elasticsearch Vector Store</p>
                <p>🤖 <strong>Model:</strong> GPT-4 Turbo</p>
                <p>🔗 <strong>Framework:</strong> LangChain Agents</p>
              </div>
            </div>

            <div>
              <p className="text-sm font-bold text-gray-700 mb-2">🏆 Why Elastic?</p>
              <div className="bg-blue-50 border border-blue-100 rounded-lg p-3 text-xs text-blue-800 space-y-1.5">
                <p><strong>⚡ Powered by Elasticsearch RAG</strong></p>
                <p>Unlike chatbots limited by context size:</p>
                <p>📦 <strong>Scale:</strong> Index <strong>thousands</strong> of PDFs, not just one.</p>
                <p>🎯 <strong>Precision:</strong> Find exact regulations in milliseconds.</p>
                <p>🔒 <strong>Privacy:</strong> Data stays in your private vectors.</p>
              </div>
            </div>

            {/* Active Docs */}
            {indexedFiles.length > 0 && (
              <div>
                <hr className="border-gray-200 mb-3" />
                <p className="text-sm font-bold text-gray-700 mb-2">🗂️ Active Docs</p>
                <div className="space-y-1.5">
                  {indexedFiles.map((f, i) => (
                    <div key={i} className="bg-green-50 border border-green-200 rounded-lg px-2.5 py-1.5 text-xs text-green-700 flex items-center gap-2">
                      <span>📄</span><span className="truncate">{f}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            <hr className="border-gray-200" />

            {/* Architecture Button */}
            <button
              onClick={() => window.open("/Arc_diagram/architecture_pro.html", "_blank")}
              className="w-full py-2 text-sm font-bold bg-gradient-to-r from-[#8b5cf6] to-[#7c3aed] text-white rounded-lg hover:shadow-md transition-all"
            >
              🛠️ Architecture
            </button>

            <hr className="border-gray-200" />
            <p className="text-[10px] text-gray-400 text-center">© 2026 JurisLens Inc. | <strong>Privacy Policy</strong></p>
          </div>
        </aside>
      </div>
    </div>
  );
}
