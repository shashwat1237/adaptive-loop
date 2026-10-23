import React from "react";
import { Protocol } from "../lib/types";
import { Pill, Dumbbell, Sparkles, Utensils } from "lucide-react";

interface Props {
  protocols: Protocol[];
  overallAdherence: number;
}

export const ProtocolSummary: React.FC<Props> = ({ protocols, overallAdherence }) => {
  const getCategoryIcon = (category: string) => {
    switch (category) {
      case "SUPPLEMENT":
        return Pill;
      case "EXERCISE":
        return Dumbbell;
      case "NUTRITION":
        return Utensils;
      default:
        return Sparkles;
    }
  };

  const getAdherenceBadgeColor = (rate: number) => {
    if (rate >= 80) return "text-emerald-400 bg-emerald-500/10 border-emerald-500/30";
    if (rate >= 50) return "text-amber-400 bg-amber-500/10 border-amber-500/30";
    return "text-rose-400 bg-rose-500/10 border-rose-500/30";
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
      <div className="flex items-center justify-between mb-4">
        <h3 className="font-semibold text-white text-sm flex items-center gap-2">
          <span>Active Personalized Protocols</span>
          <span className="text-xs px-2 py-0.5 rounded-full bg-slate-800 text-slate-400">
            {protocols.length}
          </span>
        </h3>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Adherence (180d):</span>
          <span
            className={`text-xs px-2.5 py-1 rounded-full border font-mono font-semibold ${getAdherenceBadgeColor(
              overallAdherence
            )}`}
          >
            {overallAdherence}%
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {protocols.map((p) => {
          const Icon = getCategoryIcon(p.category);
          return (
            <div
              key={p.id}
              className="p-3.5 rounded-lg bg-slate-950/60 border border-slate-800/80 flex items-start gap-3"
            >
              <div className="w-8 h-8 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-center shrink-0">
                <Icon className="w-4 h-4 text-sky-400" />
              </div>
              <div className="min-w-0 flex-1">
                <div className="flex items-center justify-between gap-2">
                  <h4 className="text-sm font-medium text-slate-200 truncate">{p.name}</h4>
                  <span className="text-[10px] uppercase font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-400">
                    {p.category}
                  </span>
                </div>
                <p className="text-xs text-slate-400 mt-1">{p.dosage_or_frequency}</p>
                <div className="flex items-center gap-3 mt-2 text-[11px] text-slate-500 font-mono">
                  <span>Target: {p.target_adherence_rate}%</span>
                  <span>•</span>
                  <span>Review: {p.review_date}</span>
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
