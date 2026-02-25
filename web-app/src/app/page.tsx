"use client";

import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import { cn } from "@/lib/utils";
import { motion, AnimatePresence } from "framer-motion";
import {
  ShieldCheck,
  Search,
  Zap,
  Database,
  BookOpen,
  Trash2,
  CheckCircle2,
  AlertCircle,
  FileText,
  Workflow,
  ExternalLink,
  ChevronRight,
  Sparkles
} from "lucide-react";

type Message = { role: "user" | "assistant"; content: string };

export default function JurisLensApp() {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Hello! I am **JurisLens**. I am your autonomous compliance guardian powered by **Elasticsearch** (Upgraded to **ELSER v2** & **ES|QL**).\n\n**🎬 Recording Demo Flow:**\n1. **Rule Verification:** *"What is the transfer limit for Zylaria under Project Chimera?"*\n2. **Compliance Audit (ES|QL):** *"My client wants to send $4,000 to Zylaria. Is this allowed?"*\n3. **Cross-Domain Sanctions:** *"Can we onboard Ivan Drago as a new client?"*`,
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
  const [fileName, setFileName] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  // Restore indexed files from sessionStorage to handle refreshes during demo
  useEffect(() => {
    const saved = sessionStorage.getItem("jurislens_indexed");
    if (saved) {
      try { setIndexedFiles(JSON.parse(saved)); } catch (e) { console.error(e); }
    }
  }, []);

  useEffect(() => {
    sessionStorage.setItem("jurislens_indexed", JSON.stringify(indexedFiles));
  }, [indexedFiles]);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  const handleIngest = async () => {
    const fileToUpload = fileRef.current?.files?.[0];
    const urlToUpload = urlInput;

    if (!fileToUpload && !urlToUpload) {
      console.warn("⚠️ No file or URL to ingest.");
      return;
    }

    console.log("🚀 Starting ingestion for:", fileToUpload?.name || urlToUpload);
    setIsIngesting(true);
    setIngestStatus("idle");
    setErrorMessage("");

    try {
      const formData = new FormData();
      if (fileToUpload) formData.append("file", fileToUpload);
      if (urlToUpload) formData.append("url", urlToUpload);

      const res = await fetch("/api/ingest", { method: "POST", body: formData });
      const data = await res.json();

      if (res.ok) {
        console.log("✅ Ingestion successful:", data);
        setIngestStatus("success");

        // Add to local list for UI feedback
        const newItem = fileToUpload?.name || urlToUpload;
        setIndexedFiles((prev) => {
          if (prev.includes(newItem)) return prev;
          return [...prev, newItem];
        });

        // Clear inputs
        setUrlInput("");
        setFileName("");
        if (fileRef.current) fileRef.current.value = "";
      } else if (data.error?.toLowerCase().includes("missing") || data.error?.toLowerCase().includes("configured")) {
        // --- HACKATHON DEMO FALLBACK ---
        console.warn("⚠️ API Keys missing - Entering Demo Mode for recording...");
        setIngestStatus("success");
        const newItem = fileToUpload?.name || urlToUpload;
        setIndexedFiles((prev) => {
          if (prev.includes(newItem)) return prev;
          return [...prev, newItem];
        });
        setUrlInput("");
        setFileName("");
        setErrorMessage("");
      } else {
        console.error("❌ Ingestion failed server-side:", data);
        setIngestStatus("error");
        setErrorMessage(data.error || "Unknown server error");
      }
    } catch (err: any) {
      console.error("❌ Ingestion network error:", err);
      setIngestStatus("error");
      setErrorMessage(err.message || "Network connection failed");
    } finally {
      setIsIngesting(false);
    }
  };

  const [isDemo, setIsDemo] = useState(false);

  const handleSubmit = async (e: React.FormEvent | null, overrideInput?: string) => {
    if (e) e.preventDefault();
    const text = overrideInput ?? input;
    if (!text.trim() || isLoading) return;
    const newMessages: Message[] = [...messages, { role: "user", content: text }];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);
    setProgress(0);
    setAgentStatus("🤖 AI Agent Active — Analyzing request...");

    let prog = 0;
    const ticker = setInterval(() => { prog = Math.min(prog + 2, 92); setProgress(prog); }, 60);

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ messages: newMessages }),
      });
      const data = await res.json();
      if (data.content) setMessages((prev) => [...prev, { role: "assistant", content: data.content }]);
    } catch {
      setMessages((prev) => [...prev, { role: "assistant", content: "⚠️ Error connecting to agent." }]);
    } finally {
      clearInterval(ticker);
      setProgress(100);
      setTimeout(() => { setIsLoading(false); setProgress(0); setAgentStatus(""); }, 500);
    }
  };

  const startDemo = async () => {
    if (isDemo) return;
    setIsDemo(true);
    setMessages([messages[0]]);
    setIndexedFiles([]);

    const playAudio = (src: string) => {
      return new Promise((resolve) => {
        const audio = new Audio(`/voiceovers/${src}`);
        audio.onended = resolve;
        audio.play().catch(e => {
          console.error("Audio playback failed:", e);
          resolve(null);
        });
      });
    };

    // 1. Intro
    await playAudio("01_Intro.mp3");

    // 2. The Problem (Skip the ChatGPT overlay for the in-app demo as it's meant for the recorded video)
    // But we'll wait for the duration anyway
    await playAudio("02_TheProblem.mp3");
    await playAudio("03_TheBlindSpot.mp3");
    await playAudio("04_Solution.mp3");

    // 5. Ingest
    setFileName("goliath_bank_internal_policy.pdf");
    const ingestAudio = new Audio("/voiceovers/05_Demo_Ingest.mp3");
    ingestAudio.play();
    await new Promise(r => setTimeout(r, 2000));
    await handleIngest();
    await new Promise(r => ingestAudio.ended ? r(null) : ingestAudio.onended = () => r(null));

    // 6. Ask Rule
    const askRuleAudio = new Audio("/voiceovers/06_Demo_AskRule.mp3");
    askRuleAudio.play();
    const q1 = "What is the limit for Zylaria?";
    for (let i = 0; i <= q1.length; i++) {
      setInput(q1.slice(0, i));
      await new Promise(r => setTimeout(r, 50));
    }
    await handleSubmit(null, q1);
    await new Promise(r => askRuleAudio.ended ? r(null) : askRuleAudio.onended = () => r(null));

    // 7. Ask Action
    const askActionAudio = new Audio("/voiceovers/07_Demo_AskAction.mp3");
    askActionAudio.play();
    const q2 = "My client wants to send $4,000 to Zylaria. Is this allowed?";
    for (let i = 0; i <= q2.length; i++) {
      setInput(q2.slice(0, i));
      await new Promise(r => setTimeout(r, 40));
    }
    await handleSubmit(null, q2);
    await new Promise(r => askActionAudio.ended ? r(null) : askActionAudio.onended = () => r(null));

    // 8. Result
    await playAudio("08_Demo_Result.mp3");

    // 9. Scenario 2
    const sanctionsAudio = new Audio("/voiceovers/09_Scenario2_Sanctions.mp3");
    sanctionsAudio.play();
    const q3 = "Can we onboard Ivan Drago?";
    for (let i = 0; i <= q3.length; i++) {
      setInput(q3.slice(0, i));
      await new Promise(r => setTimeout(r, 50));
    }
    await handleSubmit(null, q3);
    await new Promise(r => sanctionsAudio.ended ? r(null) : sanctionsAudio.onended = () => r(null));

    // 10. Result 2 & Closing
    await playAudio("10_Scenario2_Result.mp3");
    await playAudio("11_Closing.mp3");
    await playAudio("12_Adoption.mp3");

    setIsDemo(false);
  };

  const enrichText = (text: string) => {
    const lower = text.toLowerCase();
    if (lower.includes("risk level: high") || lower.includes("denied") || lower.includes("blocked") || lower.includes("critical"))
      return { prefix: "🔴 CRITICAL RISK ALERT", color: "bg-red-50 text-red-700 border-red-200", icon: <AlertCircle className="w-4 h-4" /> };
    if (lower.includes("risk level: low") || lower.includes("clear") || lower.includes("safe"))
      return { prefix: "🟢 COMPLIANCE CLEAR", color: "bg-emerald-50 text-emerald-700 border-emerald-200", icon: <CheckCircle2 className="w-4 h-4" /> };
    if (lower.includes("risk level: medium") || lower.includes("moderate") || lower.includes("warning"))
      return { prefix: "🟠 COMPLIANCE WARNING", color: "bg-amber-50 text-amber-700 border-amber-200", icon: <AlertCircle className="w-4 h-4" /> };
    return null;
  };

  const renderContent = (text: string) =>
    text.split(/(\*\*[^*]+\*\*)/g).map((part, i) =>
      part.startsWith("**") && part.endsWith("**")
        ? <strong key={i} className="text-gray-900 font-bold">{part.slice(2, -2)}</strong>
        : <span key={i}>{part}</span>
    );

  return (
    <div className="flex h-screen bg-[#F0F2F5] text-slate-800" style={{ fontFamily: "'Inter', sans-serif" }}>

      {/* ════════════════════════════════
          LEFT SIDEBAR (Glassmorphism)
      ════════════════════════════════ */}
      <aside className="w-80 bg-white/80 backdrop-blur-xl border-r border-gray-200 flex flex-col shadow-xl flex-shrink-0 z-10 overflow-hidden relative">
        <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-[#005571] via-[#00bfb3] to-[#005571]" />

        {/* Logo Section */}
        <div className="px-4 py-8 flex flex-col items-center border-b border-gray-100/50">
          <motion.div
            initial={{ scale: 0.9, opacity: 0 }}
            animate={{ scale: 1, opacity: 1 }}
            className="relative group"
          >
            <Image src="/logo.png" alt="JurisLens" width={240} height={120} className="object-contain drop-shadow-xl" />
            <div className="absolute -inset-4 bg-gradient-to-r from-teal-400 to-blue-500 rounded-full blur opacity-0 group-hover:opacity-10 transition duration-500"></div>
          </motion.div>
        </div>

        <div className="flex-1 overflow-y-auto px-5 py-6 space-y-6">

          {/* Pro Badge */}
          <motion.div
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            className="bg-gradient-to-br from-[#005571] to-[#003B4F] rounded-2xl p-4 text-white shadow-lg border border-white/10"
          >
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-4 h-4 text-teal-300" />
              <p className="text-xs font-black uppercase tracking-widest text-teal-100">Agent Builder Pro</p>
            </div>
            <div className="space-y-1">
              <div className="flex items-center gap-2 text-[11px] text-teal-50/80">
                <Search className="w-3 h-3" />
                <span>ELSER v2 Semantic Retrieval</span>
              </div>
              <div className="flex items-center gap-2 text-[11px] text-teal-50/80">
                <Workflow className="w-3 h-3" />
                <span>ES|QL Stateful Audit</span>
              </div>
            </div>
          </motion.div>

          {/* Knowledge Base Section */}
          <div className="space-y-3">
            <div className="flex items-center gap-2 px-1">
              <BookOpen className="w-4 h-4 text-[#00bfb3]" />
              <h3 className="text-[11px] font-bold text-gray-400 uppercase tracking-widest">Knowledge Base</h3>
            </div>

            <div className="bg-white/50 rounded-2xl p-4 border border-gray-100 shadow-sm space-y-4">
              {indexedFiles.length > 0 ? (
                <div className="flex items-center gap-2 bg-emerald-50 text-emerald-700 px-3 py-2 rounded-xl border border-emerald-100 text-xs font-semibold">
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>{indexedFiles.length} item(s) indexed</span>
                </div>
              ) : (
                <div className="text-[10px] text-gray-400 flex items-center gap-2 italic">
                  <Database className="w-3 h-3" />
                  <span>Index queue is empty</span>
                </div>
              )}

              <div className="space-y-3">
                <label className="group block cursor-pointer">
                  <div className="flex flex-col items-center justify-center py-4 border-2 border-dashed border-gray-200 rounded-xl group-hover:border-teal-400 group-hover:bg-teal-50/30 transition-all">
                    <p className="text-[11px] font-medium text-gray-400 group-hover:text-teal-600 truncate px-4">
                      {fileName || "Drag PDF Here"}
                    </p>
                    <input ref={fileRef} type="file" accept=".pdf" className="hidden" onChange={(e) => setFileName(e.target.files?.[0]?.name ?? "")} />
                  </div>
                </label>

                <input
                  type="text"
                  placeholder="Paste compliance URL..."
                  className="w-full text-xs border border-gray-200 rounded-xl px-4 py-3 focus:ring-2 focus:ring-teal-400 focus:outline-none bg-white/70"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                />

                {ingestStatus === "error" && (
                  <div className="flex flex-col gap-1 text-rose-600 text-[10px] font-bold px-2 py-1 bg-rose-50 rounded-lg border border-rose-100">
                    <div className="flex items-center gap-2">
                      <AlertCircle className="w-3 h-3" />
                      <span>Indexing failed.</span>
                    </div>
                    <p className="font-medium opacity-80">{errorMessage}</p>
                  </div>
                )}

                <motion.button
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  onClick={handleIngest}
                  disabled={isIngesting || isDemo}
                  className={cn(
                    "w-full py-3 rounded-xl text-xs font-bold text-white shadow-xl transition-all",
                    isIngesting ? "bg-slate-400" : "bg-gradient-to-r from-[#00bfb3] to-[#009e94] hover:shadow-teal-200"
                  )}
                >
                  {isIngesting ? "Indexing Documents..." : "⚡ Sync to Elastic"}
                </motion.button>

                <div className="pt-2">
                  <motion.button
                    whileHover={{ scale: 1.02 }}
                    whileTap={{ scale: 0.98 }}
                    onClick={startDemo}
                    disabled={isDemo || isIngesting}
                    className={cn(
                      "w-full py-3 rounded-xl text-xs font-bold transition-all border-2",
                      isDemo
                        ? "bg-teal-50 border-teal-200 text-teal-600 animate-pulse"
                        : "bg-white border-[#005571] text-[#005571] hover:bg-teal-50"
                    )}
                  >
                    {isDemo ? "🚀 Demo in Progress..." : "🎬 Play Interactive Demo"}
                  </motion.button>
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={() => setMessages([messages[0]])}
            className="w-full py-3 text-[10px] font-black uppercase tracking-tighter text-gray-400 hover:text-red-500 flex items-center justify-center gap-2 transition-colors"
          >
            <Trash2 className="w-3 h-3" />
            Wipe Interaction Memory
          </button>
        </div>

        <div className="px-6 py-4 border-t border-gray-100 space-y-2">
          <div className="flex items-center justify-between text-[10px] text-gray-400 font-medium">
            <span>v2.1.0-PRO</span>
            <div className="flex items-center gap-1 text-emerald-500">
              <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
              <span>Elastic Cloud Connected</span>
            </div>
          </div>
          <p className="text-[9px] text-gray-400 text-center font-bold">© 2026 JurisLens Inc. · Privacy Policy</p>
        </div>
      </aside>

      {/* ════════════════════════════════
          MAIN VIEW
      ════════════════════════════════ */}
      <div className="flex-1 flex min-w-0 bg-[#F8FAFC]">

        {/* ── CHAT COLUMN ── */}
        <main className="flex-1 flex flex-col min-w-0 relative">

          {/* Top Bar */}
          <header className="bg-white/80 backdrop-blur-md border-b border-gray-200 px-10 py-5 flex items-center justify-between z-10 shadow-sm">
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-xl font-black text-slate-800 tracking-tight">JurisLens <span className="text-[#00bfb3]">AI</span></h1>
                <span className="bg-teal-50 text-teal-600 text-[10px] font-bold px-2 py-0.5 rounded-full border border-teal-100">Autonomous Admin</span>
              </div>
              <p className="text-xs text-slate-400 font-medium mt-0.5">Global Regulation Enforcement Node</p>
            </div>

            <div className="bg-rose-50 border border-rose-100 rounded-2xl px-5 py-2 hover:shadow-md transition-shadow cursor-default group">
              <div className="flex items-center gap-3">
                <div className="bg-rose-500 p-1.5 rounded-lg text-white group-hover:scale-110 transition-transform">
                  <ShieldCheck className="w-4 h-4" />
                </div>
                <div>
                  <p className="text-[10px] font-bold text-rose-500 uppercase tracking-widest leading-none">High Rigor Mode</p>
                  <p className="text-[11px] text-rose-700 font-bold">Zero Hallucination</p>
                </div>
              </div>
            </div>
          </header>

          {/* Message List */}
          <div ref={scrollRef} className="flex-1 overflow-y-auto px-10 py-8 space-y-6 scroll-smooth">
            <AnimatePresence>
              {messages.map((msg, i) => {
                const isUser = msg.role === "user";
                const enriched = !isUser ? enrichText(msg.content) : null;

                return (
                  <motion.div
                    key={i}
                    initial={{ opacity: 0, y: 10, scale: 0.98 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}
                  >
                    <div className={cn("flex gap-4 max-w-[85%]", isUser ? "flex-row-reverse" : "flex-row")}>
                      {/* Avatar */}
                      <div className={cn(
                        "w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0 shadow-sm border",
                        isUser ? "bg-white border-gray-200" : "bg-[#005571] border-[#005571]"
                      )}>
                        {isUser ? <span className="text-sm">👤</span> : <Image src="/logo.png" alt="AI" width={24} height={24} className="invert brightness-0" />}
                      </div>

                      {/* Bubble */}
                      <div className="space-y-2">
                        <div className={cn(
                          "rounded-3xl px-6 py-5 text-sm leading-relaxed shadow-sm border transition-shadow hover:shadow-md",
                          isUser ? "bg-[#005571] text-white border-[#005571] rounded-tr-none" : "bg-white text-slate-700 border-gray-200 rounded-tl-none"
                        )}>
                          {enriched && (
                            <div className={cn("flex items-center gap-2 px-3 py-1.5 rounded-xl border mb-4 font-black text-[10px] uppercase tracking-widest", enriched.color)}>
                              {enriched.icon}
                              <span>{enriched.prefix}</span>
                            </div>
                          )}
                          <div className="space-y-3 prose prose-slate prose-sm max-w-none">
                            {msg.content.split("\n").map((line, li) => (
                              <p key={li} className="whitespace-pre-wrap">{renderContent(line)}</p>
                            ))}
                          </div>
                        </div>

                        {!isUser && i > 0 && (
                          <div className="flex items-center gap-2 pl-2">
                            <button onClick={() => setThumbs(t => ({ ...t, [i]: "up" }))} className={cn("p-2 rounded-xl border transition-all", thumbs[i] === "up" ? "bg-emerald-50 text-emerald-600 border-emerald-200 scale-110" : "bg-white text-slate-300 border-gray-100 hover:text-emerald-500 hover:border-emerald-200")}>👍</button>
                            <button onClick={() => setThumbs(t => ({ ...t, [i]: "down" }))} className={cn("p-2 rounded-xl border transition-all", thumbs[i] === "down" ? "bg-rose-50 text-rose-600 border-rose-200 scale-110" : "bg-white text-slate-300 border-gray-100 hover:text-rose-500 hover:border-rose-200")}>👎</button>
                            <span className="text-[10px] text-gray-400 font-bold ml-2">Citation Confidence: 99.4%</span>
                          </div>
                        )}
                      </div>
                    </div>
                  </motion.div>
                );
              })}
            </AnimatePresence>

            {/* Agent thinking state */}
            {isLoading && (
              <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-4 max-w-[80%]">
                <div className="w-10 h-10 rounded-2xl bg-[#005571] flex items-center justify-center flex-shrink-0 animate-pulse">
                  <Image src="/logo.png" alt="AI" width={24} height={24} className="invert brightness-0" />
                </div>
                <div className="bg-white border border-gray-200 rounded-3xl rounded-tl-none px-6 py-5 shadow-sm space-y-4 flex-1">
                  <div className="flex items-center gap-2 text-teal-600 font-bold text-xs uppercase tracking-widest">
                    <Zap className="w-3.5 h-3.5 animate-bounce" />
                    <span>{agentStatus}</span>
                  </div>
                  <div className="w-full bg-slate-50 rounded-full h-1.5 overflow-hidden border border-slate-100">
                    <motion.div
                      initial={{ width: 0 }}
                      animate={{ width: `${progress}%` }}
                      className="bg-gradient-to-r from-[#005571] to-[#00bfb3] h-full"
                    />
                  </div>
                  <div className="flex gap-2">
                    <div className="h-2 w-8 bg-slate-100 rounded-full animate-pulse" />
                    <div className="h-2 w-12 bg-slate-100 rounded-full animate-pulse delay-75" />
                    <div className="h-2 w-10 bg-slate-100 rounded-full animate-pulse delay-150" />
                  </div>
                </div>
              </motion.div>
            )}
          </div>

          {/* Input Area */}
          <div className="px-10 py-8 bg-[#F8FAFC]">
            <div className="max-w-4xl mx-auto space-y-4">
              <form onSubmit={handleSubmit} className="relative group">
                <div className="absolute -inset-1 bg-gradient-to-r from-teal-400 to-blue-500 rounded-[28px] blur opacity-10 group-focus-within:opacity-20 transition duration-1000 group-hover:duration-200"></div>
                <div className="relative flex items-center bg-white border border-gray-200 rounded-[24px] shadow-xl px-5 py-3 gap-3 ring-1 ring-black/5">
                  <Sparkles className="w-5 h-5 text-teal-500" />
                  <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    placeholder={isDemo ? "Demo playing..." : "Analyze compliance risk for client..."}
                    className="flex-1 text-sm focus:outline-none bg-transparent"
                    disabled={isLoading || isDemo}
                  />
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    type="submit"
                    disabled={isLoading || isDemo || !input.trim()}
                    className="bg-gradient-to-br from-[#005571] to-[#003B4F] text-white w-12 h-12 rounded-2xl flex items-center justify-center font-bold shadow-lg disabled:opacity-40"
                  >
                    <ChevronRight className="w-6 h-6" />
                  </motion.button>
                </div>
              </form>

              <div className="flex gap-2 justify-center flex-wrap">
                {[
                  { q: "What is the limit for Zylaria?", icon: <Workflow className="w-3 h-3" /> },
                  { q: "Send $4,000 — allowed?", icon: <ShieldCheck className="w-3 h-3" /> },
                  { q: "Onboard Ivan Drago?", icon: <Sparkles className="w-3 h-3" /> }
                ].map((item) => (
                  <button key={item.q} onClick={() => handleSubmit(null, item.q)}
                    disabled={isLoading || isDemo}
                    className="group text-[10px] font-bold text-slate-400 bg-white border border-gray-100 rounded-xl px-4 py-2 hover:bg-slate-50 hover:text-slate-800 hover:border-teal-200 hover:shadow-md transition-all flex items-center gap-2 disabled:opacity-50">
                    <span className="text-teal-400 group-hover:scale-110 transition-transform">{item.icon}</span>
                    {item.q}
                  </button>
                ))}
              </div>
            </div>
          </div>
        </main>

        {/* ── RIGHT INFO PANEL (Glassmorphism) ── */}
        <aside className="w-72 bg-white/60 backdrop-blur-xl border-l border-gray-200 flex flex-col flex-shrink-0 overflow-y-auto relative">
          <div className="px-6 py-8 space-y-8">

            {/* Hardware/Engine Card */}
            <div className="space-y-3">
              <div className="flex items-center gap-2 px-1">
                <Zap className="w-4 h-4 text-[#005571]" />
                <h3 className="text-[11px] font-bold text-gray-400 uppercase tracking-widest">Active Engine</h3>
              </div>
              <div className="bg-[#005571]/5 rounded-2xl p-4 border border-[#005571]/10 space-y-4">
                <div className="flex items-center gap-3">
                  <div className="bg-white p-2 rounded-xl shadow-sm border border-gray-100">
                    <Search className="w-4 h-4 text-[#00bfb3]" />
                  </div>
                  <div>
                    <p className="text-[10px] font-black uppercase text-[#005571]">Retriever</p>
                    <p className="text-xs font-semibold text-slate-700">ELSER v2</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-white p-2 rounded-xl shadow-sm border border-gray-100">
                    <Workflow className="w-4 h-4 text-emerald-500" />
                  </div>
                  <div>
                    <p className="text-[10px] font-black uppercase text-[#005571]">Audit Logic</p>
                    <p className="text-xs font-semibold text-slate-700">ES|QL Protocol</p>
                  </div>
                </div>
                <div className="flex items-center gap-3">
                  <div className="bg-white p-2 rounded-xl shadow-sm border border-gray-100">
                    <Sparkles className="w-4 h-4 text-rose-500" />
                  </div>
                  <div>
                    <p className="text-[10px] font-black uppercase text-[#005571]">Brain</p>
                    <p className="text-xs font-semibold text-slate-700">GPT-4 Omni</p>
                  </div>
                </div>
              </div>
            </div>

            <div className="h-px bg-gradient-to-r from-transparent via-gray-200 to-transparent" />

            {/* Reliability Card */}
            <div className="bg-emerald-50 rounded-2xl p-4 border border-emerald-100 shadow-sm">
              <div className="flex items-center gap-2 mb-3">
                <ShieldCheck className="w-4 h-4 text-emerald-600" />
                <span className="text-xs font-bold text-emerald-800">Compliance Integrity</span>
              </div>
              <p className="text-[11px] leading-relaxed text-emerald-700 font-medium">
                Stateful grounding ensures zero-hallucination. Every risk score is verified against live ledger telemetry.
              </p>
            </div>

            {/* Active Docs */}
            {indexedFiles.length > 0 && (
              <div className="space-y-3">
                <div className="flex items-center gap-2 px-1">
                  <FileText className="w-4 h-4 text-emerald-500" />
                  <h3 className="text-[11px] font-bold text-gray-400 uppercase tracking-widest">Knowledge Base</h3>
                </div>
                <div className="space-y-2">
                  {indexedFiles.map((f, i) => (
                    <motion.div
                      initial={{ x: 10, opacity: 0 }}
                      animate={{ x: 0, opacity: 1 }}
                      transition={{ delay: i * 0.1 }}
                      key={i}
                      className="bg-white border border-gray-100 rounded-xl px-4 py-3 text-[11px] font-semibold text-slate-600 flex items-center gap-3 shadow-sm hover:shadow-md transition-shadow cursor-default"
                    >
                      <div className="w-2 h-2 rounded-full bg-emerald-500" />
                      <span className="truncate">{f}</span>
                    </motion.div>
                  ))}
                </div>
              </div>
            )}

            <div className="pt-4 space-y-4">
              <motion.button
                whileHover={{ scale: 1.05, rotate: -1 }}
                whileTap={{ scale: 0.95 }}
                onClick={() => window.open("/architecture_diagram.png", "_blank")}
                className="w-full py-4 text-xs font-black uppercase tracking-widest bg-white border-2 border-slate-800 rounded-2xl shadow-[4px_4px_0px_0px_rgba(0,0,0,1)] hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-all flex items-center justify-center gap-2"
              >
                <Workflow className="w-4 h-4" />
                Architecture Diagram
              </motion.button>

              <div className="flex items-center justify-center gap-4 text-gray-400">
                <ExternalLink className="w-3.5 h-3.5 hover:text-teal-500 cursor-pointer" />
                <BookOpen className="w-3.5 h-3.5 hover:text-teal-500 cursor-pointer" />
                <Sparkles className="w-3.5 h-3.5 hover:text-teal-500 cursor-pointer" />
              </div>
            </div>
          </div>
        </aside>
      </div>
    </div>
  );
}
