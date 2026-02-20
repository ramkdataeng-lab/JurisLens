"use client";

import { useState, useRef, useEffect } from "react";
import { useChat } from "ai/react";
import {
  ShieldCheck,
  Search,
  FileUp,
  Database,
  Bot,
  User,
  Send,
  Loader2,
  History,
  CheckCircle2,
  AlertCircle,
  Gavel,
  ExternalLink,
  ChevronRight
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { cn } from "@/lib/utils";
import Image from "next/image";

export default function JurisLensApp() {
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestStatus, setIngestStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const [urlInput, setUrlInput] = useState("");
  const [indexedFiles, setIndexedFiles] = useState<string[]>([]);
  const scrollRef = useRef<HTMLDivElement>(null);

  const { messages, input, handleInputChange, handleSubmit, isLoading } = useChat({
    api: "/api/chat",
  });

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [messages]);

  const handleIngest = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsIngesting(true);
    setIngestStatus("loading");

    try {
      const formData = new FormData();
      if (urlInput) formData.append("url", urlInput);

      const fileInput = document.getElementById("file-upload") as HTMLInputElement;
      if (fileInput.files?.[0]) {
        formData.append("file", fileInput.files[0]);
      }

      const res = await fetch("/api/ingest", {
        method: "POST",
        body: formData,
      });

      if (res.ok) {
        setIngestStatus("success");
        if (urlInput) setIndexedFiles(prev => [...prev, urlInput]);
        if (fileInput.files?.[0]) setIndexedFiles(prev => [...prev, fileInput.files![0].name]);
        setUrlInput("");
        fileInput.value = "";
      } else {
        setIngestStatus("error");
      }
    } catch (err) {
      setIngestStatus("error");
    } finally {
      setIsIngesting(false);
      setTimeout(() => setIngestStatus("idle"), 3000);
    }
  };

  return (
    <div className="flex h-screen bg-[#0f172a] text-slate-200 font-sans overflow-hidden">
      {/* --- Sidebar --- */}
      <aside className="w-80 bg-[#1e293b] border-r border-slate-700/50 flex flex-col shadow-2xl z-10">
        <div className="p-6 border-b border-slate-700/50 flex items-center gap-3 bg-gradient-to-r from-slate-900/50 to-transparent">
          <div className="bg-indigo-600 p-2 rounded-lg shadow-lg shadow-indigo-500/20">
            <ShieldCheck className="w-6 h-6 text-white" />
          </div>
          <div>
            <h1 className="text-xl font-bold tracking-tight text-white italic">JurisLens</h1>
            <p className="text-[10px] text-slate-400 font-mono uppercase tracking-widest">Autonomous Compliance</p>
          </div>
        </div>

        <div className="flex-1 overflow-y-auto p-4 space-y-8 py-8">
          {/* Knowledge Base Section */}
          <section className="space-y-4">
            <div className="flex items-center gap-2 text-indigo-400 font-semibold px-2">
              <Database className="w-4 h-4" />
              <h2 className="text-sm uppercase tracking-wider">Storage & Retrieval</h2>
            </div>

            <div className="bg-slate-800/50 rounded-xl p-4 border border-slate-700/50 space-y-4">
              <div>
                <label className="text-[11px] text-slate-400 uppercase mb-2 block font-medium">Regulation Source (PDF)</label>
                <label htmlFor="file-upload" className="flex items-center justify-center gap-2 w-full p-3 rounded-lg border-2 border-dashed border-slate-600 hover:border-indigo-500 hover:bg-slate-700/50 transition-all cursor-pointer group">
                  <FileUp className="w-4 h-4 text-slate-400 group-hover:text-indigo-400" />
                  <span className="text-xs text-slate-300">Choose File</span>
                  <input id="file-upload" type="file" className="hidden" />
                </label>
              </div>

              <div>
                <label className="text-[11px] text-slate-400 uppercase mb-2 block font-medium">External Policy (URL)</label>
                <input
                  type="text"
                  placeholder="https://..."
                  className="w-full bg-slate-900/50 border border-slate-600 rounded-lg p-3 text-xs focus:ring-2 focus:ring-indigo-500 focus:outline-none transition-all"
                  value={urlInput}
                  onChange={(e) => setUrlInput(e.target.value)}
                />
              </div>

              <button
                onClick={handleIngest}
                disabled={isIngesting}
                className={cn(
                  "w-full py-3 rounded-lg text-sm font-bold flex items-center justify-center gap-2 transition-all active:scale-95 shadow-lg shadow-indigo-900/20",
                  ingestStatus === "success" ? "bg-emerald-600 text-white" :
                    ingestStatus === "error" ? "bg-rose-600 text-white" :
                      "bg-indigo-600 text-white hover:bg-indigo-500"
                )}
              >
                {isIngesting ? <Loader2 className="w-4 h-4 animate-spin" /> :
                  ingestStatus === "success" ? <CheckCircle2 className="w-4 h-4" /> :
                    ingestStatus === "error" ? <AlertCircle className="w-4 h-4" /> :
                      <CheckCircle2 className="w-4 h-4" />}
                {isIngesting ? "Indexing..." :
                  ingestStatus === "success" ? "Indexed!" :
                    ingestStatus === "error" ? "Failed" :
                      "Process & Index"}
              </button>
            </div>
          </section>

          {/* Active Documents List */}
          {indexedFiles.length > 0 && (
            <section className="space-y-4">
              <div className="flex items-center gap-2 text-indigo-400 font-semibold px-2">
                <History className="w-4 h-4" />
                <h2 className="text-sm uppercase tracking-wider">Active Corpus</h2>
              </div>
              <div className="space-y-2">
                {indexedFiles.map((file, idx) => (
                  <motion.div
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    key={idx}
                    className="p-3 bg-slate-800/30 rounded-lg border border-slate-700/30 text-[11px] flex items-center gap-2 hover:bg-slate-800/60 transition-colors"
                  >
                    <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 shadow-[0_0_8px_rgba(16,185,129,0.5)]" />
                    <span className="truncate flex-1 text-slate-300">{file}</span>
                  </motion.div>
                ))}
              </div>
            </section>
          )}
        </div>

        <div className="p-6 border-t border-slate-700/50 bg-slate-900/30">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center font-bold text-white shadow-lg">JD</div>
            <div>
              <p className="text-sm font-bold text-white leading-none mb-1">Jon Doe</p>
              <p className="text-[10px] text-slate-500 font-medium">Enterprise Admin</p>
            </div>
          </div>
        </div>
      </aside>

      {/* --- Main Chat Area --- */}
      <main className="flex-1 flex flex-col relative">
        <header className="h-20 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50 flex items-center justify-between px-8 z-10">
          <div className="flex items-center gap-4">
            <div className="flex items-center gap-2 text-slate-400">
              <Bot className="w-5 h-5 text-indigo-400" />
              <span className="text-sm font-medium tracking-wide uppercase">JurisLens Expert Agent</span>
            </div>
            <div className="hidden md:flex items-center gap-2 bg-emerald-500/10 text-emerald-400 text-[10px] font-bold px-2 py-1 rounded-full border border-emerald-500/20 tracking-tighter uppercase ring-1 ring-emerald-500/20">
              <span className="flex h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
              Elasticsearch Core Optimized
            </div>
          </div>
        </header>

        {/* Messages */}
        <div ref={scrollRef} className="flex-1 overflow-y-auto p-8 space-y-6 scroll-smooth">
          {messages.length === 0 ? (
            <div className="h-full flex flex-col items-center justify-center text-center space-y-8 max-w-2xl mx-auto">
              <motion.div
                initial={{ scale: 0.8, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="relative"
              >
                <div className="absolute -inset-4 bg-indigo-500/20 blur-3xl rounded-full" />
                <Image src="/logo.png" alt="Logo" width={100} height={100} className="relative opacity-60 grayscale hover:grayscale-0 transition-all duration-500 animate-pulse-slow" />
              </motion.div>
              <div className="space-y-4">
                <h2 className="text-4xl font-black text-white tracking-tight leading-tight">
                  Autonomous Compliance <br />
                  <span className="text-indigo-400">Guardian</span>
                </h2>
                <p className="text-slate-400 leading-relaxed text-lg">
                  Ask complex regulatory questions, verify ledger state, and scan international sanctions.
                  JurisLens bridges the gap between static policy and live enterprise data.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 w-full">
                <button className="p-4 bg-slate-800/40 rounded-2xl border border-slate-700/50 text-left hover:border-indigo-500/50 transition-all group">
                  <span className="block text-indigo-400 text-xs font-bold uppercase mb-2 tracking-widest leading-none">Scenario: Regulation</span>
                  <p className="text-sm text-slate-200">"What is the transfer limit under Project Chimera?"</p>
                </button>
                <button className="p-4 bg-slate-800/40 rounded-2xl border border-slate-700/50 text-left hover:border-indigo-500/50 transition-all group">
                  <span className="block text-indigo-400 text-xs font-bold uppercase mb-2 tracking-widest leading-none">Scenario: Risk Ledger</span>
                  <p className="text-sm text-slate-200">"Check risk for $4,000 transfer to Zylaria."</p>
                </button>
              </div>
            </div>
          ) : (
            messages.map((m, idx) => (
              <motion.div
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                key={m.id}
                className={cn(
                  "flex gap-4 max-w-4xl mx-auto",
                  m.role === "user" ? "flex-row-reverse" : ""
                )}
              >
                <div className={cn(
                  "p-2 rounded-xl flex-shrink-0 h-10 w-10 flex items-center justify-center shadow-lg",
                  m.role === "user" ? "bg-slate-700 text-slate-200" : "bg-indigo-600 text-white"
                )}>
                  {m.role === "user" ? <User className="w-5 h-5" /> : <ShieldCheck className="w-5 h-5" />}
                </div>

                <div className={cn(
                  "flex-1 p-5 rounded-3xl text-sm leading-relaxed shadow-xl border",
                  m.role === "user"
                    ? "bg-slate-800 border-slate-700 text-slate-200"
                    : "bg-gradient-to-br from-indigo-900/40 to-slate-900 border-indigo-500/20 text-slate-100"
                )}>
                  {/* Dynamic coloring for results */}
                  <div className="prose prose-invert prose-sm max-w-none">
                    {m.content.split('\n').map((line, i) => (
                      <p key={i} className={cn(
                        "mb-2 whitespace-pre-wrap",
                        line.toLowerCase().includes("high risk") || line.toLowerCase().includes("denied") || line.toLowerCase().includes("blocked") ? "text-rose-400 font-bold bg-rose-400/10 p-2 rounded-lg border border-rose-400/20 shadow-[0_0_15px_rgba(251,113,133,0.1)]" :
                          line.toLowerCase().includes("low risk") || line.toLowerCase().includes("clear") || line.toLowerCase().includes("safe") ? "text-emerald-400 font-bold" : ""
                      )}>
                        {line}
                      </p>
                    ))}
                  </div>
                </div>
              </motion.div>
            ))
          )}

          {isLoading && (
            <div className="flex gap-4 max-w-4xl mx-auto items-center">
              <div className="bg-indigo-600 p-2 rounded-xl h-10 w-10 flex items-center justify-center animate-pulse">
                <Loader2 className="w-5 h-5 animate-spin" />
              </div>
              <div className="flex gap-1">
                <div className="w-1 h-1 rounded-full bg-slate-500 animate-bounce [animation-delay:-0.3s]" />
                <div className="w-1 h-1 rounded-full bg-slate-500 animate-bounce [animation-delay:-0.15s]" />
                <div className="w-1 h-1 rounded-full bg-slate-500 animate-bounce" />
              </div>
            </div>
          )}
        </div>

        {/* Input Bar */}
        <div className="p-8 bg-gradient-to-t from-slate-900 via-slate-900/80 to-transparent">
          <form
            onSubmit={handleSubmit}
            className="max-w-4xl mx-auto relative group"
          >
            <div className="absolute -inset-2 bg-indigo-500/20 blur-xl opacity-0 group-focus-within:opacity-100 transition-opacity rounded-full transition-all duration-500" />
            <div className="relative bg-slate-800/80 border border-slate-700 flex items-center p-2 rounded-2xl shadow-2xl backdrop-blur-sm group-focus-within:border-indigo-500/50 transition-all ring-1 ring-slate-700/50 group-focus-within:ring-indigo-500/20">
              <input
                type="text"
                className="flex-1 bg-transparent border-none focus:outline-none p-4 text-sm text-white placeholder-slate-500"
                placeholder="Ask JurisLens something... e.g., 'Is a $6,000 transfer to Zylaria allowed?'"
                value={input}
                onChange={handleInputChange}
              />
              <button
                type="submit"
                disabled={isLoading || !input.trim()}
                className="bg-indigo-600 p-4 rounded-xl text-white hover:bg-indigo-500 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg shadow-indigo-600/30 active:scale-95"
              >
                <Send className="w-5 h-5" />
              </button>
            </div>
          </form>
          <div className="mt-4 flex justify-center gap-6 text-[10px] text-slate-500 uppercase font-bold tracking-widest opacity-50">
            <span className="flex items-center gap-1"><ShieldCheck className="w-3 h-3" /> SOC2 Compliant</span>
            <span className="flex items-center gap-1"><Gavel className="w-3 h-3" /> Audit Logged</span>
            <span className="flex items-center gap-1 tracking-tighter"><Image src="/logo.png" alt="E" width={10} height={10} className="filter grayscale" /> Powered by Elastic Cloud</span>
          </div>
        </div>
      </main>
    </div>
  );
}
