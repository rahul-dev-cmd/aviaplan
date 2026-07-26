"use client";

import React, { useState } from "react";
import { Plane, Compass, Sparkles, IndianRupee, MapPin, ChevronDown, AlertCircle } from "lucide-react";

interface TripFormProps {
  onSubmit: (data: { query: string; origin?: string; destination?: string; max_budget?: number }) => void;
  isLoading: boolean;
}

const CITIES = [
  { name: "Delhi", code: "DEL" },
  { name: "Mumbai", code: "BOM" },
  { name: "Bangalore", code: "BLR" },
  { name: "Chennai", code: "MAA" },
  { name: "Kolkata", code: "CCU" },
  { name: "Hyderabad", code: "HYD" },
  { name: "Goa", code: "GOA" },
];

export default function TripForm({ onSubmit, isLoading }: TripFormProps) {
  const [query, setQuery] = useState("");
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [budget, setBudget] = useState("");

  const presetQueries = [
    { label: "🌴 Weekend in Goa under ₹15k", query: "Plan a weekend trip to Goa under ₹15,000, leaving Friday", origin: "DEL", dest: "GOA", b: "15000" },
    { label: "🏙️ Mumbai to Goa Speed Trip", query: "Quick 2-day getaway from Mumbai to Goa under ₹10,000", origin: "BOM", dest: "GOA", b: "10000" },
    { label: "💼 Bangalore to Delhi Budget", query: "Fly from Bangalore to Delhi under ₹12,000", origin: "BLR", dest: "DEL", b: "12000" }
  ];

  const handleOriginChange = (selectedOrigin: string) => {
    setOrigin(selectedOrigin);
    if (selectedOrigin && selectedOrigin === destination) {
      setDestination("");
    }
  };

  const handleDestinationChange = (selectedDest: string) => {
    setDestination(selectedDest);
    if (selectedDest && selectedDest === origin) {
      setOrigin("");
    }
  };

  const isSameCity = Boolean(origin && destination && origin === destination);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (isSameCity) return;

    const trimmedQuery = query.trim();
    const finalQuery = trimmedQuery || (origin && destination ? `Fly from ${origin} to ${destination}${budget ? ' with budget ₹' + budget : ''}` : "Plan a flight trip");
    
    onSubmit({
      query: finalQuery,
      origin: origin ? origin.toUpperCase() : undefined,
      destination: destination ? destination.toUpperCase() : undefined,
      max_budget: budget ? parseFloat(budget) : undefined,
    });
  };

  const handleSelectPreset = (preset: typeof presetQueries[0]) => {
    setQuery(preset.query);
    setOrigin(preset.origin);
    setDestination(preset.dest);
    setBudget(preset.b);
  };

  return (
    <div className="w-full max-w-4xl mx-auto bg-white/90 backdrop-blur-md rounded-2xl p-6 md:p-8 shadow-xl border border-cream-200">
      <div className="flex items-center space-x-3 mb-6">
        <div className="w-10 h-10 rounded-xl bg-airline-orange/10 flex items-center justify-center text-airline-orange">
          <Plane className="w-6 h-6" />
        </div>
        <div>
          <h2 className="text-xl font-bold text-slate-800 tracking-tight">Autonomous Flight & Trip Planner</h2>
          <p className="text-xs text-slate-500">Provide one high-level prompt or specify exact route parameters.</p>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="space-y-5">
        {/* Main Prompt Bar */}
        <div>
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wider mb-2 flex items-center gap-1.5">
            <Sparkles className="w-3.5 h-3.5 text-airline-sky" /> High-Level Instruction
          </label>
          <div className="relative">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Enter instruction (e.g. Plan a 3-day trip from Delhi to Goa under ₹15,000)..."
              className="w-full px-4 py-3.5 pl-11 bg-cream-50/70 border border-slate-200 rounded-xl text-slate-900 text-sm focus:outline-none focus:ring-2 focus:ring-airline-sky/40 focus:border-airline-sky transition"
            />
            <Compass className="w-5 h-5 text-slate-400 absolute left-3.5 top-3.5" />
          </div>
        </div>

        {/* Quick Presets */}
        <div>
          <span className="text-[11px] font-medium text-slate-400 uppercase tracking-wider block mb-2">Quick Presets</span>
          <div className="flex flex-wrap gap-2">
            {presetQueries.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSelectPreset(preset)}
                className="text-xs px-3 py-1.5 rounded-lg bg-cream-100/70 hover:bg-airline-sky/10 hover:text-airline-sky border border-slate-200/70 text-slate-700 transition font-medium"
              >
                {preset.label}
              </button>
            ))}
          </div>
        </div>

        {/* Precision Route & Budget Grid */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 border-t border-slate-100">
          {/* Origin Dropdown */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-600 uppercase mb-1 flex items-center gap-1">
              <MapPin className="w-3 h-3 text-airline-sky" /> Origin Airport
            </label>
            <div className="relative">
              <select
                value={origin}
                onChange={(e) => handleOriginChange(e.target.value)}
                className="w-full px-3 py-2 pr-8 bg-cream-50/50 border border-slate-200 rounded-lg text-xs text-slate-900 font-semibold focus:outline-none focus:border-airline-sky focus:ring-1 focus:ring-airline-sky/40 cursor-pointer appearance-none transition"
              >
                <option value="">Select Origin</option>
                {CITIES.map((city) => (
                  <option
                    key={city.code}
                    value={city.code}
                    disabled={city.code === destination}
                  >
                    {city.name} ({city.code})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
            </div>
          </div>

          {/* Destination Dropdown */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-600 uppercase mb-1 flex items-center gap-1">
              <MapPin className="w-3 h-3 text-airline-orange" /> Destination
            </label>
            <div className="relative">
              <select
                value={destination}
                onChange={(e) => handleDestinationChange(e.target.value)}
                className="w-full px-3 py-2 pr-8 bg-cream-50/50 border border-slate-200 rounded-lg text-xs text-slate-900 font-semibold focus:outline-none focus:border-airline-sky focus:ring-1 focus:ring-airline-sky/40 cursor-pointer appearance-none transition"
              >
                <option value="">Select Destination</option>
                {CITIES.map((city) => (
                  <option
                    key={city.code}
                    value={city.code}
                    disabled={city.code === origin}
                  >
                    {city.name} ({city.code})
                  </option>
                ))}
              </select>
              <ChevronDown className="w-4 h-4 text-slate-400 absolute right-2.5 top-2.5 pointer-events-none" />
            </div>
          </div>

          {/* Budget Input */}
          <div>
            <label className="block text-[11px] font-semibold text-slate-600 uppercase mb-1 flex items-center gap-1">
              <IndianRupee className="w-3 h-3 text-emerald-600" /> Max Target Budget (₹)
            </label>
            <input
              type="number"
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              placeholder="e.g. 15000"
              className="w-full px-3 py-2 bg-cream-50/50 border border-slate-200 rounded-lg text-xs text-slate-900 font-semibold focus:outline-none focus:border-airline-sky"
            />
          </div>
        </div>

        {/* Same City Validation Message */}
        {isSameCity && (
          <div className="flex items-center gap-1.5 text-xs text-rose-600 font-medium bg-rose-50 border border-rose-200 p-2.5 rounded-lg">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>Origin and destination cannot be the same city. Please select different airports.</span>
          </div>
        )}

        {/* Submit CTA */}
        <button
          type="submit"
          disabled={isLoading || isSameCity}
          className="w-full py-4 bg-airline-orange hover:bg-orange-700 text-white font-bold rounded-xl shadow-lg shadow-airline-orange/20 transition flex items-center justify-center space-x-2 text-sm disabled:opacity-50 cursor-pointer"
        >
          <Plane className="w-5 h-5 animate-pulse" />
          <span>{isLoading ? "Agents Planning Flight & Trip..." : "Dispatch Autonomous Agent Pipeline"}</span>
        </button>
      </form>
    </div>
  );
}
