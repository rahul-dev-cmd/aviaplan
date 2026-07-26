"use client";

import React, { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { Plane, Cloud, CheckCircle2, Sparkles } from "lucide-react";

const TRAVELER_STEPS = [
  "Understanding your travel preferences...",
  "Searching best direct & connecting flights...",
  "Finding top-rated hotels & stays...",
  "Checking local weather forecast...",
  "Optimizing flight & hotel packages within budget...",
  "Finalizing your custom boarding pass & itinerary..."
];

interface TakeoffLoaderProps {
  isComplete?: boolean;
}

export default function TakeoffLoader({ isComplete = false }: TakeoffLoaderProps) {
  const [stepIndex, setStepIndex] = useState(0);

  useEffect(() => {
    if (isComplete) {
      setStepIndex(TRAVELER_STEPS.length - 1);
      return;
    }

    const interval = setInterval(() => {
      setStepIndex((prev) => (prev < TRAVELER_STEPS.length - 1 ? prev + 1 : prev));
    }, 700);

    return () => clearInterval(interval);
  }, [isComplete]);

  const activeStep = isComplete ? TRAVELER_STEPS.length - 1 : stepIndex;
  const progressPercent = Math.round(((activeStep + 1) / TRAVELER_STEPS.length) * 100);

  return (
    <div className="w-full max-w-2xl mx-auto bg-gradient-to-b from-white via-cream-50/80 to-amber-50/30 rounded-2xl p-6 md:p-8 border border-cream-200 shadow-xl text-center space-y-6">
      {/* Traveler-Facing Title Header */}
      <div className="space-y-1">
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-airline-sky/10 text-airline-sky text-xs font-bold border border-airline-sky/20">
          <Sparkles className="w-3.5 h-3.5" />
          <span>Finding your best trip...</span>
        </div>
        <h3 className="text-xl font-bold text-slate-800 tracking-tight pt-1">
          {isComplete ? "Your Itinerary is Ready!" : "Crafting Your Perfect Route"}
        </h3>
      </div>

      {/* Runway & Takeoff Animation (Light Cream & Sky Background) */}
      <div className="relative w-full h-48 bg-gradient-to-r from-sky-100/70 via-cream-50 to-orange-50/70 rounded-2xl overflow-hidden border border-cream-200 shadow-inner flex flex-col justify-between p-4">
        {/* Floating Clouds Background */}
        <div className="relative w-full h-12 overflow-hidden">
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: "-30%" }}
            transition={{ duration: 12, repeat: Infinity, ease: "linear" }}
            className="absolute top-1 text-slate-400/40"
          >
            <Cloud className="w-9 h-9" />
          </motion.div>
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: "-30%" }}
            transition={{ duration: 8, delay: 2, repeat: Infinity, ease: "linear" }}
            className="absolute top-4 text-sky-400/30"
          >
            <Cloud className="w-12 h-12" />
          </motion.div>
          <motion.div
            initial={{ x: "100%" }}
            animate={{ x: "-30%" }}
            transition={{ duration: 15, delay: 5, repeat: Infinity, ease: "linear" }}
            className="absolute top-2 text-amber-400/20"
          >
            <Cloud className="w-7 h-7" />
          </motion.div>
        </div>

        {/* Animated Jet Airplane with Takeoff Trajectory & Speed Lines */}
        <div className="relative w-full h-24 overflow-hidden flex items-end">
          <motion.div
            className="absolute left-0 flex items-center gap-2"
            animate={
              isComplete
                ? { x: "110%", y: -70, rotate: -25 }
                : {
                    x: ["-15%", "35%", "85%", "110%"],
                    y: [15, 0, -35, -60],
                    rotate: [0, -10, -20, -28],
                  }
            }
            transition={{
              duration: 3.2,
              repeat: isComplete ? 0 : Infinity,
              ease: "easeInOut",
            }}
          >
            {/* Speed Lines */}
            <motion.div
              animate={{ opacity: [0.2, 0.9, 0.2], scaleX: [0.8, 1.3, 0.8] }}
              transition={{ duration: 0.5, repeat: Infinity }}
              className="flex gap-1 items-center"
            >
              <div className="w-8 h-[2px] bg-gradient-to-r from-transparent to-airline-orange rounded-full" />
              <div className="w-5 h-[2px] bg-airline-sky rounded-full" />
            </motion.div>

            {/* Jet Airplane Icon */}
            <div className="w-11 h-11 rounded-full bg-white shadow-lg border border-orange-200 flex items-center justify-center text-airline-orange">
              <Plane className="w-6 h-6 transform rotate-45" />
            </div>
          </motion.div>
        </div>

        {/* Runway Ground Line */}
        <div className="w-full h-3 border-t-2 border-dashed border-amber-300/80 flex items-center justify-around px-2">
          <div className="w-10 h-1 bg-amber-400/60 rounded-full" />
          <div className="w-10 h-1 bg-amber-400/60 rounded-full" />
          <div className="w-10 h-1 bg-amber-400/60 rounded-full" />
          <div className="w-10 h-1 bg-amber-400/60 rounded-full" />
          <div className="w-10 h-1 bg-amber-400/60 rounded-full" />
        </div>
      </div>

      {/* Progress Bar & Stage Indicator */}
      <div className="space-y-3">
        <div className="w-full bg-cream-100 rounded-full h-2.5 overflow-hidden border border-slate-200/60">
          <motion.div
            className="h-full bg-gradient-to-r from-airline-sky to-airline-orange rounded-full"
            initial={{ width: "15%" }}
            animate={{ width: `${progressPercent}%` }}
            transition={{ duration: 0.4 }}
          />
        </div>

        {/* Active Stage Label */}
        <div className="bg-cream-50 p-4 rounded-xl border border-cream-200 flex items-center space-x-3 text-left shadow-sm">
          <CheckCircle2 className={`w-5 h-5 text-airline-sky shrink-0 ${isComplete ? "" : "animate-spin"}`} />
          <div className="flex-1">
            <span className="text-[11px] font-bold uppercase tracking-wider text-airline-sky block">
              Step {activeStep + 1} of {TRAVELER_STEPS.length} {isComplete && "— Complete"}
            </span>
            <p className="text-xs font-semibold text-slate-800">{TRAVELER_STEPS[activeStep]}</p>
          </div>
          <span className="text-xs font-bold text-slate-500 bg-white px-2.5 py-1 rounded-lg border border-slate-200">
            {progressPercent}%
          </span>
        </div>
      </div>
    </div>
  );
}
