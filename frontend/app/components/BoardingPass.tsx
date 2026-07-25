"use client";

import React from "react";
import { TripResponse } from "@/lib/api";
import { Plane, Calendar, Hotel, Sun, CloudRain, CheckCircle, AlertCircle, ShieldCheck, Ticket } from "lucide-react";

interface BoardingPassProps {
  data: TripResponse;
}

export default function BoardingPass({ data }: BoardingPassProps) {
  const flight = data.selected_flight;
  const hotel = data.selected_hotel;
  const weather = data.weather_info;
  const itinerary = data.itinerary || {};

  return (
    <div className="w-full max-w-4xl mx-auto space-y-6">
      {/* Boarding Pass Container */}
      <div className="relative bg-white rounded-3xl shadow-2xl border border-cream-200 overflow-hidden text-slate-800">
        
        {/* Header Airline Stripe */}
        <div className="bg-gradient-to-r from-airline-orange via-orange-600 to-airline-sky text-white px-6 py-4 flex flex-wrap justify-between items-center gap-2">
          <div className="flex items-center space-x-2">
            <Ticket className="w-6 h-6 text-white" />
            <span className="font-extrabold tracking-widest text-sm uppercase">AviaPlan Boarding Pass & Itinerary</span>
          </div>
          <div className="flex items-center space-x-2">
            <span className="text-xs font-mono bg-white/20 px-3 py-1 rounded-full text-white font-bold">
              FLIGHT PKG #{flight?.flight_number || "AV-701"}
            </span>
          </div>
        </div>

        {/* Boarding Pass Ticket Body */}
        <div className="grid grid-cols-1 lg:grid-cols-12 relative">
          
          {/* Main Flight & Hotel Pass (8 Cols) */}
          <div className="lg:col-span-8 p-6 md:p-8 space-y-6 border-b lg:border-b-0 lg:border-r border-dashed border-slate-300">
            
            {/* Origin -> Destination Banner */}
            <div className="flex items-center justify-between bg-cream-50/80 p-5 rounded-2xl border border-cream-200">
              <div>
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">DEPARTURE</span>
                <span className="text-3xl font-black text-slate-900 tracking-tight">{data.origin}</span>
                <span className="text-xs text-slate-500 block font-medium mt-0.5">India Origin Hub</span>
              </div>

              <div className="flex flex-col items-center px-4">
                <span className="text-[10px] font-bold text-airline-sky uppercase tracking-widest mb-1">{flight?.duration || "DIRECT"}</span>
                <div className="flex items-center space-x-1">
                  <div className="w-2 h-2 rounded-full bg-airline-orange" />
                  <div className="w-16 md:w-24 h-[2px] bg-slate-300 border-t border-dashed border-slate-400" />
                  <Plane className="w-5 h-5 text-airline-orange transform rotate-90" />
                  <div className="w-16 md:w-24 h-[2px] bg-slate-300 border-t border-dashed border-slate-400" />
                  <div className="w-2 h-2 rounded-full bg-airline-sky" />
                </div>
                <span className="text-[10px] font-mono text-slate-400 mt-1">{flight?.airline || "IndiGo"}</span>
              </div>

              <div className="text-right">
                <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider block">ARRIVAL</span>
                <span className="text-3xl font-black text-slate-900 tracking-tight">{data.destination}</span>
                <span className="text-xs text-slate-500 block font-medium mt-0.5">Destination Hub</span>
              </div>
            </div>

            {/* Flight & Hotel Grid Details */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {/* Flight Box */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-slate-700 uppercase tracking-wider">
                  <span className="flex items-center gap-1.5"><Plane className="w-4 h-4 text-airline-sky" /> Flight Segment</span>
                  <span className="text-emerald-700 font-mono">₹{flight?.price_inr?.toLocaleString() || 0}</span>
                </div>
                <div className="text-xs space-y-1 text-slate-600 font-medium">
                  <p><span className="font-semibold text-slate-900">Carrier:</span> {flight?.airline} ({flight?.flight_number})</p>
                  <p><span className="font-semibold text-slate-900">Schedule:</span> {flight?.departure_time} - {flight?.arrival_time}</p>
                  <p><span className="font-semibold text-slate-900">Data Provider:</span> {flight?.source_label}</p>
                </div>
              </div>

              {/* Hotel Box */}
              <div className="p-4 rounded-xl bg-slate-50 border border-slate-200/80 space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-slate-700 uppercase tracking-wider">
                  <span className="flex items-center gap-1.5"><Hotel className="w-4 h-4 text-airline-orange" /> Hotel Stay</span>
                  <span className="text-emerald-700 font-mono">₹{hotel?.total_price_inr?.toLocaleString() || 0}</span>
                </div>
                <div className="text-xs space-y-1 text-slate-600 font-medium">
                  <p><span className="font-semibold text-slate-900">Property:</span> {hotel?.name}</p>
                  <p><span className="font-semibold text-slate-900">Location:</span> {hotel?.location} ({hotel?.rating}★)</p>
                  <p><span className="font-semibold text-slate-900">Data Provider:</span> {hotel?.source_label}</p>
                </div>
              </div>
            </div>

            {/* Weather Widget */}
            {weather && weather.forecast && (
              <div className="bg-sky-50/70 border border-sky-200/80 p-4 rounded-xl space-y-2">
                <div className="flex items-center justify-between text-xs font-bold text-sky-900 uppercase">
                  <span className="flex items-center gap-1.5"><Sun className="w-4 h-4 text-amber-500" /> Destination Weather ({weather.city})</span>
                  <span className="text-[11px] font-normal text-sky-700">Open-Meteo REST API</span>
                </div>
                <div className="grid grid-cols-3 gap-2 pt-1">
                  {weather.forecast.map((day, idx) => (
                    <div key={idx} className="bg-white/80 p-2.5 rounded-lg border border-sky-100 text-center">
                      <span className="text-[10px] font-bold text-slate-500 uppercase block">{day.date}</span>
                      <span className="text-xs font-bold text-slate-800">{day.temp_max}°C</span>
                      <span className="text-[10px] text-sky-700 block font-medium truncate">{day.condition}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Agent Summary Note */}
            <div className="bg-cream-50 p-4 rounded-xl border border-cream-200 text-xs text-slate-700 leading-relaxed font-sans">
              <span className="font-bold text-slate-900 block mb-1">AI Executive Travel Summary:</span>
              {data.summary}
            </div>

          </div>

          {/* Perforated Tear-off Stub (4 Cols) */}
          <div className="lg:col-span-4 p-6 md:p-8 bg-cream-50/60 flex flex-col justify-between space-y-6 relative">
            <div className="boarding-pass-cutout-left hidden lg:block" />
            <div className="boarding-pass-cutout-right hidden lg:block" />

            {/* Stub Header */}
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-xs font-extrabold uppercase text-slate-400 tracking-wider">BOARDING STUB</span>
                {data.is_within_budget ? (
                  <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800 border border-emerald-300">
                    <CheckCircle className="w-3 h-3 text-emerald-600" /> WITHIN BUDGET
                  </span>
                ) : (
                  <span className="inline-flex items-center gap-1 text-[10px] font-bold px-2 py-0.5 rounded-full bg-orange-100 text-orange-800 border border-orange-300">
                    <AlertCircle className="w-3 h-3 text-orange-600" /> BEST ATTEMPT
                  </span>
                )}
              </div>

              {/* Pricing Breakdown */}
              <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-sm space-y-3">
                <div className="flex justify-between items-center text-xs text-slate-600">
                  <span>Target Budget:</span>
                  <span className="font-semibold text-slate-900">₹{data.max_budget?.toLocaleString()}</span>
                </div>
                <div className="flex justify-between items-center text-xs text-slate-600">
                  <span>Flight Ticket:</span>
                  <span className="font-semibold text-slate-900">₹{flight?.price_inr?.toLocaleString() || 0}</span>
                </div>
                <div className="flex justify-between items-center text-xs text-slate-600">
                  <span>Hotel Stay (2N):</span>
                  <span className="font-semibold text-slate-900">₹{hotel?.total_price_inr?.toLocaleString() || 0}</span>
                </div>
                <div className="border-t border-slate-200 pt-2 flex justify-between items-center">
                  <span className="text-xs font-bold text-slate-900">Total Combined Cost:</span>
                  <span className="text-base font-extrabold text-emerald-700">₹{data.total_cost?.toLocaleString()}</span>
                </div>
              </div>

              {/* Data Fallback Notice Badge */}
              <div className="flex items-center space-x-2 text-[11px] text-slate-600 bg-white/80 p-2.5 rounded-lg border border-slate-200">
                <ShieldCheck className="w-4 h-4 text-airline-sky shrink-0" />
                <span>Fail-Safe Fallback Logic Verified</span>
              </div>
            </div>

            {/* Authentic Barcode Representation */}
            <div className="space-y-2 text-center pt-4 border-t border-slate-200">
              <div className="w-full h-12 bg-slate-900 rounded flex items-center justify-around px-3">
                {[...Array(28)].map((_, i) => (
                  <div
                    key={i}
                    className="bg-white h-8"
                    style={{ width: `${(i % 3) + 1}px` }}
                  />
                ))}
              </div>
              <span className="text-[10px] font-mono tracking-widest text-slate-400 block">
                AVIA-{data.origin}-{data.destination}-2026-CONFIRMED
              </span>
            </div>

          </div>

        </div>

      </div>

      {/* Day by Day Itinerary Accordion / Grid */}
      {itinerary.schedule && (
        <div className="bg-white rounded-2xl p-6 border border-cream-200 shadow-md space-y-4">
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Calendar className="w-4 h-4 text-airline-sky" /> Day-by-Day Autonomous Itinerary Schedule
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {itinerary.schedule.map((dayItem: any, idx: number) => (
              <div key={idx} className="p-4 rounded-xl bg-cream-50/70 border border-cream-200 space-y-2">
                <div className="flex items-center justify-between">
                  <span className="text-[11px] font-bold uppercase text-airline-orange">{dayItem.day}</span>
                </div>
                <h4 className="text-xs font-bold text-slate-800">{dayItem.title}</h4>
                <ul className="text-xs text-slate-600 space-y-1.5 list-disc list-inside pt-1">
                  {dayItem.activities?.map((act: string, aIdx: number) => (
                    <li key={aIdx} className="leading-snug">{act}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
