import React from "react";
import { AnalystPayload } from "../lib/types";
import { Brain, HelpCircle, Layers, CheckCircle2, Bookmark } from "lucide-react";

interface Props {
  analystPayload?: AnalystPayload;
}

export const AnalystReportCard: React.FC<Props> = ({ analystPayload }) => {
  if (!analystPayload) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-center text-xs text-slate-500">
        No AI Analyst synthesis available.
      </div>
    );
  }

  const getConfidenceBadge = (confidence: string) => {
    switch (confidence) {
      case "HIGH":
        return "bg-emerald-500/10 text-emerald-400 border-emerald-500/30";
      case "MODERATE":
        return "bg-sky-500/10 text-sky-400 border-sky-500/30";
      default:
        return "bg-amber-500/10 text-amber-400 border-amber-500/30";
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <h3 className="font-semibold text-white text-sm flex items-center gap-2">
          <Brain className="w-4 h-4 text-sky-400" />
          <span>Stage 2: AI Analyst Reasoning Ledger</span>
        </h3>
        <span className="text-[11px] text-slate-400 font-mono">
          Initial: <strong className="text-slate-200">{analystPayload.initial_action_recommendation}</strong>
        </span>
      </div>

      {/* Primary Hypothesis */}
      <div className="p-4 rounded-lg bg-sky-950/20 border border-sky-800/40 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs uppercase tracking-wider font-semibold text-sky-400 flex items-center gap-1.5">
            <CheckCircle2 className="w-3.5 h-3.5" />
            Primary Intervention Hypothesis
          </span>
          <span
            className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getConfidenceBadge(
              analystPayload.primary_hypothesis.confidence
            )}`}
          >
            {analystPayload.primary_hypothesis.confidence} CONFIDENCE
          </span>
        </div>
        <p className="text-sm text-slate-200 leading-relaxed">
          {analystPayload.primary_hypothesis.statement}
        </p>

        <div className="flex flex-wrap items-center gap-1.5 pt-2">
          <span className="text-[11px] text-slate-400 flex items-center gap-1 mr-1">
            <Bookmark className="w-3 h-3 text-sky-400" /> Grounded Citations:
          </span>
          {analystPayload.primary_hypothesis.cited_observations.map((cid) => (
            <span
              key={cid}
              className="text-[10px] font-mono px-2 py-0.5 rounded bg-slate-900 text-sky-300 border border-slate-700 hover:border-sky-500 transition-colors cursor-pointer"
            >
              {cid}
            </span>
          ))}
        </div>
      </div>

      {/* Competing Hypotheses */}
      {analystPayload.competing_hypotheses.length > 0 && (
        <div className="space-y-2.5">
          <h4 className="text-xs uppercase tracking-wider font-semibold text-slate-400 flex items-center gap-1.5">
            <Layers className="w-3.5 h-3.5 text-slate-500" />
            Competing / Alternative Hypotheses
          </h4>
          {analystPayload.competing_hypotheses.map((ch, idx) => (
            <div
              key={idx}
              className="p-3.5 rounded-lg bg-slate-950/60 border border-slate-800/80 space-y-1.5"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-medium text-slate-300">Alternative Hypothesis #{idx + 1}</span>
                <span
                  className={`text-[10px] font-mono px-2 py-0.5 rounded-full border ${getConfidenceBadge(
                    ch.confidence
                  )}`}
                >
                  {ch.confidence}
                </span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">{ch.statement}</p>
              <div className="flex flex-wrap items-center gap-1.5 pt-1">
                {ch.cited_observations.map((cid) => (
                  <span
                    key={cid}
                    className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-900 text-slate-400 border border-slate-800"
                  >
                    {cid}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Uncertainties */}
      {analystPayload.unresolved_uncertainties.length > 0 && (
        <div className="p-3 rounded-lg bg-slate-950/40 border border-slate-800/60 space-y-1">
          <h4 className="text-xs font-semibold text-slate-400 flex items-center gap-1.5">
            <HelpCircle className="w-3.5 h-3.5 text-amber-400" /> Explicit Epistemic Uncertainties
          </h4>
          <ul className="list-disc list-inside space-y-0.5 text-xs text-slate-400 pl-1">
            {analystPayload.unresolved_uncertainties.map((u, i) => (
              <li key={i}>{u}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};
