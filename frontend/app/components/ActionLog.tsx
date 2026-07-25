"use client";

import React from "react";
import { ActionLogItem } from "@/lib/api";
import { Terminal, AlertTriangle, Zap, CheckCircle, Info, RefreshCw } from "lucide-react";

interface ActionLogProps {
  logs: ActionLogItem[];
}

export default function ActionLog({ logs }: ActionLogProps) {
  if (!logs || logs.length === 0) return null;

  const getStatusBadge = (status: string) => {
    switch (status.toUpperCase()) {
      case "SUCCESS":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 border border-emerald-300">
            <CheckCircle className="w-3 h-3 text-emerald-600" /> SUCCESS
          </span>
        );
      case "FALLBACK":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded bg-amber-100 text-amber-900 border border-amber-300 animate-pulse">
            <Zap className="w-3 h-3 text-amber-600 fill-amber-500" /> LIVE API FALLBACK
          </span>
        );
      case "WARNING":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded bg-orange-100 text-orange-800 border border-orange-300">
            <AlertTriangle className="w-3 h-3 text-orange-600" /> DEGRADED ROUTE
          </span>
        );
      case "RETRY":
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded bg-sky-100 text-sky-800 border border-sky-300">
            <RefreshCw className="w-3 h-3 text-sky-600" /> BUDGET RETRY
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded bg-slate-100 text-slate-700 border border-slate-300">
            <Info className="w-3 h-3 text-slate-500" /> INFO
          </span>
        );
    }
  };

  return (
    <div className="w-full bg-slate-900 text-slate-100 rounded-2xl p-6 shadow-2xl border border-slate-800 space-y-4">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-800 pb-3">
        <div className="flex items-center space-x-2.5">
          <div className="w-7 h-7 rounded-lg bg-airline-orange/20 flex items-center justify-center text-airline-orange">
            <Terminal className="w-4 h-4" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-100 tracking-wide">Agent Execution Audit Log</h3>
            <p className="text-[11px] text-slate-400">Transparent timeline of state graph nodes, tool invocations, & API fallbacks</p>
          </div>
        </div>
        <span className="text-[10px] font-mono px-2.5 py-1 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
          {logs.length} Operations Logged
        </span>
      </div>

      {/* Log Feed */}
      <div className="space-y-2.5 max-h-[380px] overflow-y-auto pr-2 font-mono text-xs scrollbar-thin">
        {logs.map((log, index) => (
          <div
            key={index}
            className={`p-3 rounded-xl border transition ${
              log.status === "FALLBACK"
                ? "bg-amber-950/30 border-amber-800/60"
                : log.status === "WARNING"
                ? "bg-orange-950/30 border-orange-800/60"
                : "bg-slate-800/50 border-slate-800 hover:border-slate-700"
            }`}
          >
            <div className="flex flex-wrap items-center justify-between gap-2 mb-1">
              <div className="flex items-center space-x-2">
                <span className="text-[11px] text-slate-400 font-semibold">{log.timestamp}</span>
                <span className="text-[10px] uppercase font-bold text-airline-sky px-1.5 py-0.5 rounded bg-airline-sky/10 border border-airline-sky/20">
                  {log.node}
                </span>
                {getStatusBadge(log.status)}
              </div>
            </div>
            <p className="text-slate-200 text-xs leading-relaxed font-sans mt-1">
              {log.message}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}
