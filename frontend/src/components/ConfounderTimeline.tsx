import React from "react";
import { ConfounderEvent } from "../lib/types";
import { AlertCircle, Plane, Thermometer, Briefcase, Zap } from "lucide-react";

interface Props {
  confounders: ConfounderEvent[];
}

export const ConfounderTimeline: React.FC<Props> = ({ confounders }) => {
  const getEventIcon = (type: string) => {
    switch (type) {
      case "ILLNESS":
        return Thermometer;
      case "TRAVEL":
        return Plane;
      case "LIFE_STRESS":
        return Briefcase;
      default:
        return Zap;
    }
  };

  const getSeverityBadge = (severity: string) => {
    switch (severity) {
      case "SEVERE":
        return "bg-rose-500/10 text-rose-400 border-rose-500/30";
      case "MODERATE":
        return "bg-amber-500/10 text-amber-400 border-amber-500/30";
      default:
        return "bg-slate-500/10 text-slate-400 border-slate-500/30";
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-white text-sm flex items-center gap-2">
          <span>Acute Confounders & Lifestyle Shifts</span>
          <span
            className={`text-xs px-2 py-0.5 rounded-full ${
              confounders.length > 0
                ? "bg-amber-500/20 text-amber-300 font-mono"
                : "bg-slate-800 text-slate-400 font-mono"
            }`}
          >
            {confounders.length} {confounders.length === 1 ? "Event" : "Events"}
          </span>
        </h3>
      </div>

      {confounders.length === 0 ? (
        <div className="py-6 text-center text-xs text-slate-500 bg-slate-950/40 rounded-lg border border-slate-800/60">
          No acute confounding events recorded. Physiological signals have high baseline consistency.
        </div>
      ) : (
        <div className="space-y-3">
          {confounders.map((c) => {
            const Icon = getEventIcon(c.event_type);
            return (
              <div
                key={c.id}
                className="p-3.5 rounded-lg bg-slate-950/60 border border-slate-800/80 flex items-start gap-3"
              >
                <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center shrink-0">
                  <Icon className="w-4 h-4 text-amber-400" />
                </div>
                <div className="min-w-0 flex-1">
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-mono text-xs font-semibold text-slate-300">
                      {c.id} • {c.event_type.replace("_", " ")}
                    </span>
                    <span
                      className={`text-[10px] uppercase font-mono px-2 py-0.5 rounded-full border ${getSeverityBadge(
                        c.severity
                      )}`}
                    >
                      {c.severity}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mt-1.5">{c.description}</p>
                  <p className="text-[11px] text-slate-500 font-mono mt-2">
                    Active Window: {c.start_date} to {c.end_date}
                  </p>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
};
