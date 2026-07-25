"use client";

import React, { useEffect, useState } from "react";
import { Plane, Cloud, CheckCircle2 } from "lucide-react";

const AGENT_STEPS = [
  "Parsing high-level natural language prompt into sub-tasks...",
  "Querying RapidAPI Skyscanner endpoint for live flight options...",
  "Searching RapidAPI Booking.com endpoint for accommodations...",
  "Fetching 3-day meteorological forecast from Open-Meteo REST service...",
  "Evaluating combined itinerary cost against target budget threshold...",
  "Synthesizing final boarding pass & day-by-day travel itinerary..."
];

export default function TakeoffLoader() {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    const interval = setInterval(() => {
      setStepIndex((prev) => (prev < AGENT_STEPS.length - 1 ? prev + 1 : prev));
    }, 700);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="w-full max-w-2xl mx-auto bg-white rounded-2xl p-8 border border-cream-200 shadow-xl text-center space-y-6">
      <div className="flex justify-center items-center gap-2 text-airline-sky font-semibold text-xs tracking-wider uppercase">
        <Plane className="w-4 h-4" /> Agentic AI Execution In Progress
      </div>

      {/* Runway Animation Container */}
      <div className="relative w-full h-44 bg-slate-900 rounded-xl overflow-hidden shadow-inner border border-slate-800 flex flex-col justify-between p-4">
        {/* Sky / Clouds */}
        <div className="flex justify-between items-center text-slate-700 px-4 pt-2">
          <Cloud className="w-8 h-8 opacity-40 animate-pulse" />
          <Cloud className="w-10 h-10 opacity-30" />
          <Cloud className="w-6 h-6 opacity-50" />
        </div>

        {/* Jet Airplane Accelerating & Taking Off */}
        <div className="relative w-full h-16 flex items-center">
          <div className="animate-takeoff text-airline-orange flex items-center gap-1 drop-shadow-[0_0_12px_rgba(234,88,12,0.8)]">
            <Plane className="w-9 h-9 transform rotate-[15deg]" />
            <div className="w-12 h-[2px] bg-gradient-to-r from-transparent to-airline-orange opacity-70" />
          </div>
        </div>

        {/* Runway Markings */}
        <div className="w-full h-5 border-t-2 border-dashed border-slate-600/60 flex items-center justify-around px-2">
          <div className="w-12 h-1 bg-amber-400/80 rounded-full" />
          <div className="w-12 h-1 bg-amber-400/80 rounded-full" />
          <div className="w-12 h-1 bg-amber-400/80 rounded-full" />
          <div className="w-12 h-1 bg-amber-400/80 rounded-full" />
          <div className="w-12 h-1 bg-amber-400/80 rounded-full" />
        </div>
      </div>

      {/* Dynamic Agent Step Log Message */}
      <div className="bg-cream-50 p-4 rounded-xl border border-cream-200 flex items-center space-x-3 text-left">
        <CheckCircle2 className="w-5 h-5 text-airline-sky shrink-0 animate-spin" />
        <div>
          <span className="text-[11px] font-bold uppercase tracking-wider text-airline-sky block">
            Step {stepIndex + 1} of {AGENT_STEPS.length}
          </span>
          <p className="text-xs font-medium text-slate-800">{AGENT_STEPS[stepIndex]}</p>
        </div>
      </div>
    </div>
  );
}
