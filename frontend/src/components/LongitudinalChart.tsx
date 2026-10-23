"use client";

import React, { useState } from "react";
import {
  ResponsiveContainer,
  ComposedChart,
  Line,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  Legend,
  CartesianGrid,
  ReferenceArea,
} from "recharts";
import { WeeklyRollup, ConfounderEvent, BiomarkerObservation } from "../lib/types";
import { Activity, Moon, Heart, Flame } from "lucide-react";

interface Props {
  weeklyRollups: WeeklyRollup[];
  confounders: ConfounderEvent[];
  biomarkers: BiomarkerObservation[];
}

export const LongitudinalChart: React.FC<Props> = ({
  weeklyRollups,
  confounders,
  biomarkers,
}) => {
  const [activeMetric, setActiveMetric] = useState<"ALL" | "RECOVERY" | "SLEEP">("ALL");

  const chartData = weeklyRollups.map((wr) => ({
    week: `W${wr.week_number.toString().padStart(2, "0")}`,
    weekNum: wr.week_number,
    hrv: wr.avg_hrv_rmssd,
    rhr: wr.avg_resting_heart_rate,
    totalSleep: wr.avg_total_sleep_hours,
    deepSleep: wr.avg_deep_sleep_hours,
    strain: wr.avg_strain_score,
    adherence: wr.adherence_rate,
  }));

  const getWeekFromDate = (dateStr: string) => {
    const d = new Date(dateStr);
    const start = new Date("2026-04-01");
    const diffDays = Math.floor((d.getTime() - start.getTime()) / (1000 * 60 * 60 * 24));
    return Math.max(1, Math.min(26, Math.floor(diffDays / 7) + 1));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div>
          <h3 className="font-semibold text-white text-sm flex items-center gap-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <span>180-Day Longitudinal Biometric Trajectory</span>
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Synchronized weekly rolling averages across 26 protocol weeks
          </p>
        </div>

        <div className="flex items-center gap-1.5 p-1 rounded-lg bg-slate-950 border border-slate-800 text-xs">
          <button
            onClick={() => setActiveMetric("ALL")}
            className={`px-3 py-1 rounded-md transition-colors ${
              activeMetric === "ALL"
                ? "bg-slate-800 text-white font-medium shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            All Signals
          </button>
          <button
            onClick={() => setActiveMetric("RECOVERY")}
            className={`px-3 py-1 rounded-md transition-colors ${
              activeMetric === "RECOVERY"
                ? "bg-slate-800 text-emerald-400 font-medium shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            HRV & RHR
          </button>
          <button
            onClick={() => setActiveMetric("SLEEP")}
            className={`px-3 py-1 rounded-md transition-colors ${
              activeMetric === "SLEEP"
                ? "bg-slate-800 text-sky-400 font-medium shadow-sm"
                : "text-slate-400 hover:text-white"
            }`}
          >
            Sleep Architecture
          </button>
        </div>
      </div>

      {/* Chart Canvas */}
      <div className="h-80 w-full pt-2">
        <ResponsiveContainer width="100%" height="100%">
          <ComposedChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
            <XAxis
              dataKey="week"
              stroke="#64748b"
              fontSize={11}
              tickLine={false}
              axisLine={{ stroke: "#334155" }}
            />
            {/* Left Axis: HRV & RHR */}
            <YAxis
              yAxisId="left"
              stroke="#64748b"
              fontSize={11}
              domain={[20, 90]}
              tickLine={false}
              axisLine={{ stroke: "#334155" }}
            />
            {/* Right Axis: Sleep Hours */}
            <YAxis
              yAxisId="right"
              orientation="right"
              stroke="#64748b"
              fontSize={11}
              domain={[0, 10]}
              tickLine={false}
              axisLine={{ stroke: "#334155" }}
            />

            <Tooltip
              contentStyle={{
                backgroundColor: "#0b0f17",
                borderColor: "#334155",
                borderRadius: "8px",
                fontSize: "12px",
                boxShadow: "0 10px 15px -3px rgba(0, 0, 0, 0.5)",
              }}
            />
            <Legend wrapperStyle={{ fontSize: "12px", paddingTop: "12px" }} />

            {/* Confounder Overlay Areas */}
            {confounders.map((c) => {
              const startW = `W${getWeekFromDate(c.start_date).toString().padStart(2, "0")}`;
              const endW = `W${getWeekFromDate(c.end_date).toString().padStart(2, "0")}`;
              return (
                <ReferenceArea
                  key={c.id}
                  yAxisId="left"
                  x1={startW}
                  x2={endW}
                  fill={c.event_type === "ILLNESS" ? "#f43f5e" : "#f59e0b"}
                  fillOpacity={0.12}
                  stroke={c.event_type === "ILLNESS" ? "#f43f5e" : "#f59e0b"}
                  strokeOpacity={0.3}
                  strokeDasharray="2 2"
                />
              );
            })}

            {/* Metrics */}
            {(activeMetric === "ALL" || activeMetric === "RECOVERY") && (
              <>
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="hrv"
                  name="HRV (RMSSD, ms)"
                  stroke="#10b981"
                  strokeWidth={2.5}
                  dot={{ r: 2, fill: "#10b981" }}
                  activeDot={{ r: 5 }}
                />
                <Line
                  yAxisId="left"
                  type="monotone"
                  dataKey="rhr"
                  name="Resting HR (bpm)"
                  stroke="#f43f5e"
                  strokeWidth={2}
                  strokeDasharray="3 3"
                  dot={{ r: 2, fill: "#f43f5e" }}
                />
              </>
            )}

            {(activeMetric === "ALL" || activeMetric === "SLEEP") && (
              <>
                <Area
                  yAxisId="right"
                  type="monotone"
                  dataKey="totalSleep"
                  name="Total Sleep (hrs)"
                  fill="#0ea5e9"
                  fillOpacity={0.15}
                  stroke="#0ea5e9"
                  strokeWidth={1.5}
                />
                <Line
                  yAxisId="right"
                  type="monotone"
                  dataKey="deepSleep"
                  name="Deep Sleep (hrs)"
                  stroke="#a855f7"
                  strokeWidth={2.5}
                  dot={{ r: 2, fill: "#a855f7" }}
                />
              </>
            )}
          </ComposedChart>
        </ResponsiveContainer>
      </div>

      {/* Lab Baseline vs Follow-up Comparison Banner */}
      <div className="pt-3 border-t border-slate-800">
        <h4 className="text-xs font-semibold text-slate-400 mb-2">
          Biomarker Lab Anchors (Day 0 Baseline vs Day 180 Follow-up)
        </h4>
        <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2.5">
          {Array.from(new Set(biomarkers.map((b) => b.marker_code))).map((code) => {
            const base = biomarkers.find((b) => b.marker_code === code && b.test_cycle_day === 0);
            const fol = biomarkers.find((b) => b.marker_code === code && b.test_cycle_day === 180);
            if (!base) return null;
            const delta = fol ? (((fol.value - base.value) / base.value) * 100).toFixed(1) : null;
            const isNegative = delta && parseFloat(delta) < 0;

            return (
              <div
                key={code}
                className="p-2.5 rounded-lg bg-slate-950/60 border border-slate-800 text-xs"
              >
                <div className="flex items-center justify-between text-slate-400">
                  <span className="font-semibold text-slate-200">{base.marker_name}</span>
                  <span className="font-mono text-[10px] text-slate-500">{code}</span>
                </div>
                <div className="flex items-baseline justify-between mt-1.5">
                  <span className="font-mono text-slate-400">
                    {base.value} <span className="text-[10px]">D0</span>
                  </span>
                  <span className="text-slate-600">→</span>
                  <span className="font-mono text-white font-semibold">
                    {fol ? fol.value : "--"} <span className="text-[10px]">D180</span>
                  </span>
                </div>
                {delta && (
                  <div className="mt-1 text-right">
                    <span
                      className={`text-[10px] font-mono px-1.5 py-0.5 rounded ${
                        isNegative
                          ? "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20"
                          : "bg-sky-500/10 text-sky-400 border border-sky-500/20"
                      }`}
                    >
                      {parseFloat(delta) > 0 ? `+${delta}%` : `${delta}%`}
                    </span>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
};
