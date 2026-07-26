"use client";

import React from "react";
import { ActivitiesInfo } from "../../lib/api";
import { Compass, Utensils, MapPin, Sparkles } from "lucide-react";

interface ThingsToDoProps {
  activities?: ActivitiesInfo;
}

export default function ThingsToDo({ activities }: ThingsToDoProps) {
  if (!activities) return null;

  const attractions = activities.attractions || [];
  const food = activities.food_recommendations || [];

  if (attractions.length === 0 && food.length === 0) return null;

  const cityName = activities.city_name || activities.city_code || "Destination";

  return (
    <div className="bg-white rounded-2xl p-6 border border-cream-200 shadow-md space-y-6">
      <div className="flex items-center justify-between border-b border-cream-200 pb-3">
        <div className="flex items-center space-x-2.5">
          <div className="w-8 h-8 rounded-xl bg-airline-orange/10 flex items-center justify-center text-airline-orange">
            <Compass className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-sm font-bold text-slate-900 tracking-tight">
              Things to Do in {cityName}
            </h3>
            <p className="text-[11px] text-slate-500">
              Handpicked local attractions and food recommendations
            </p>
          </div>
        </div>
        <span className="text-[10px] font-bold px-2.5 py-1 rounded-full bg-cream-100 text-slate-700 border border-slate-200 flex items-center gap-1">
          <Sparkles className="w-3 h-3 text-airline-orange" /> Curated Experiences
        </span>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Attractions Section */}
        {attractions.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center space-x-2 text-xs font-bold text-slate-800 uppercase tracking-wider">
              <MapPin className="w-4 h-4 text-airline-sky" />
              <span>Top Attractions ({attractions.length})</span>
            </div>
            <div className="space-y-2.5">
              {attractions.map((item, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl bg-cream-50/70 border border-cream-200 hover:border-airline-sky/40 transition space-y-1"
                >
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="text-xs font-bold text-slate-900">{item.name}</h4>
                    <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-airline-sky/10 text-airline-sky border border-airline-sky/20 shrink-0">
                      {item.category}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-600 leading-snug font-medium">
                    {item.short_description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Food Recommendations Section */}
        {food.length > 0 && (
          <div className="space-y-3">
            <div className="flex items-center space-x-2 text-xs font-bold text-slate-800 uppercase tracking-wider">
              <Utensils className="w-4 h-4 text-airline-orange" />
              <span>Must-Try Dining ({food.length})</span>
            </div>
            <div className="space-y-2.5">
              {food.map((item, idx) => (
                <div
                  key={idx}
                  className="p-3.5 rounded-xl bg-cream-50/70 border border-cream-200 hover:border-airline-orange/40 transition space-y-1"
                >
                  <div className="flex items-center justify-between gap-2">
                    <h4 className="text-xs font-bold text-slate-900">{item.name}</h4>
                    <span className="text-[9px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-amber-100 text-amber-800 border border-amber-300 shrink-0">
                      {item.cuisine_type}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-600 leading-snug font-medium">
                    {item.short_description}
                  </p>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
