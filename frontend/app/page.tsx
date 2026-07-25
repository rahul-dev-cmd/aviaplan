"use client";

import React, { useState } from "react";
import TripForm from "./components/TripForm";
import TakeoffLoader from "./components/TakeoffLoader";
import BoardingPass from "./components/BoardingPass";
import ActionLog from "./components/ActionLog";
import { planTrip, TripResponse } from "@/lib/api";
import { Plane, Terminal, Sparkles, RefreshCw } from "lucide-react";

export default function Home() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<TripResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<"pass" | "log">("pass");

  const handleFormSubmit = async (payload: {
    query: string;
    origin?: string;
    destination?: string;
    max_budget?: number;
  }) => {
    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const response = await planTrip(payload);
      setResult(response);
    } catch (err: any) {
      setError(err.message || "Failed to execute trip plan.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="min-h-screen bg-cream-50 text-slate-800 pb-16">
      {/* Airline Header Navigation */}
      <header className="border-b border-cream-200 bg-white/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-6xl mx-auto px-4 py-3.5 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-airline-orange to-airline-sky flex items-center justify-center text-white shadow-md">
              <Plane className="w-5 h-5" />
            </div>
            <div>
              <span className="font-black text-lg text-slate-900 tracking-tight block leading-none">AviaPlan</span>
              <span className="text-[10px] font-bold text-airline-orange uppercase tracking-wider">Autonomous Trip Agent</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <span className="text-[11px] font-semibold px-3 py-1 rounded-full bg-cream-100 text-slate-700 border border-slate-200">
              Agentic AI Track
            </span>
          </div>
        </div>
      </header>

      {/* Hero Header */}
      <section className="max-w-4xl mx-auto px-4 pt-10 pb-6 text-center space-y-3">
        <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-airline-sky/10 text-airline-sky text-xs font-bold border border-airline-sky/20">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Multi-Tool LangGraph Agent with Live API Fallback</span>
        </div>
        <h1 className="text-3xl md:text-5xl font-black text-slate-900 tracking-tight leading-tight">
          Where would you like to fly?
        </h1>
        <p className="text-sm text-slate-600 max-w-xl mx-auto">
          Give one high-level prompt. Our AI agent plans flights, hotels, and weather forecasts with transparent budget optimization.
        </p>
      </section>

      {/* Main Flow Container */}
      <div className="max-w-5xl mx-auto px-4 space-y-8">
        {/* Form Container */}
        <TripForm onSubmit={handleFormSubmit} isLoading={loading} />

        {/* Loading State */}
        {loading && <TakeoffLoader />}

        {/* Error Notification */}
        {error && (
          <div className="max-w-2xl mx-auto p-4 rounded-xl bg-red-50 border border-red-200 text-red-700 text-xs font-medium text-center">
            ⚠️ {error}. Ensure your backend server is running on <code className="bg-red-100 px-1 py-0.5 rounded">http://localhost:8000</code>.
          </div>
        )}

        {/* Results Container */}
        {result && (
          <div className="space-y-6 animate-fadeIn">
            {/* View Switcher Bar */}
            <div className="flex items-center justify-between bg-white p-2 rounded-2xl border border-cream-200 shadow-sm max-w-md mx-auto">
              <button
                onClick={() => setActiveTab("pass")}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-2 ${
                  activeTab === "pass"
                    ? "bg-airline-sky text-white shadow"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                <Plane className="w-4 h-4" />
                <span>Boarding Pass & Itinerary</span>
              </button>

              <button
                onClick={() => setActiveTab("log")}
                className={`flex-1 py-2.5 px-4 rounded-xl text-xs font-bold transition flex items-center justify-center space-x-2 ${
                  activeTab === "log"
                    ? "bg-slate-900 text-white shadow"
                    : "text-slate-600 hover:text-slate-900"
                }`}
              >
                <Terminal className="w-4 h-4" />
                <span>Action Log ({result.action_logs?.length || 0})</span>
              </button>
            </div>

            {/* Tab Views */}
            {activeTab === "pass" && <BoardingPass data={result} />}
            {activeTab === "log" && <ActionLog logs={result.action_logs} />}

            {/* Bottom Action Log Embed (always shown below for full transparency) */}
            {activeTab === "pass" && (
              <div className="pt-6">
                <ActionLog logs={result.action_logs} />
              </div>
            )}
          </div>
        )}
      </div>
    </main>
  );
}
