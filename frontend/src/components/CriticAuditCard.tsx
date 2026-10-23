import React from "react";
import { CriticPayload, VerificationPayload } from "../lib/types";
import { ShieldAlert, ShieldCheck, ShieldX, Check, AlertOctagon } from "lucide-react";
import { ClinicalActionBadge } from "./ClinicalActionBadge";

interface Props {
  criticPayload?: CriticPayload;
  verificationPayload?: VerificationPayload;
}

export const CriticAuditCard: React.FC<Props> = ({ criticPayload, verificationPayload }) => {
  if (!criticPayload) {
    return (
      <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-center text-xs text-slate-500">
        No Adversarial Critic audit record available.
      </div>
    );
  }

  const getVerdictBadge = (verdict: string) => {
    switch (verdict) {
      case "APPROVED":
        return {
          icon: ShieldCheck,
          label: "VERDICT: APPROVED",
          badge: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
        };
      case "AMENDED":
        return {
          icon: ShieldAlert,
          label: "VERDICT: AMENDED",
          badge: "bg-amber-500/10 text-amber-400 border-amber-500/30",
        };
      case "REJECTED":
        return {
          icon: ShieldX,
          label: "VERDICT: REJECTED",
          badge: "bg-rose-500/10 text-rose-400 border-rose-500/30",
        };
      default:
        return {
          icon: ShieldAlert,
          label: verdict,
          badge: "bg-slate-500/10 text-slate-400 border-slate-500/30",
        };
    }
  };

  const verdictConfig = getVerdictBadge(criticPayload.verdict);
  const VerdictIcon = verdictConfig.icon;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <h3 className="font-semibold text-white text-sm flex items-center gap-2">
          <VerdictIcon className="w-4 h-4 text-amber-400" />
          <span>Stage 4: Adversarial Clinical Audit</span>
        </h3>

        <span
          className={`inline-flex items-center gap-1.5 text-xs font-mono font-bold px-3 py-1 rounded-full border ${verdictConfig.badge}`}
        >
          <VerdictIcon className="w-3.5 h-3.5" />
          {verdictConfig.label}
        </span>
      </div>

      {/* Verification Summary */}
      {verificationPayload && (
        <div className="p-3 rounded-lg bg-slate-950/60 border border-slate-800 flex items-center justify-between text-xs">
          <div className="flex items-center gap-2 text-slate-300">
            <Check className="w-4 h-4 text-emerald-400" />
            <span>Deterministic Citations:</span>
            <span className="font-mono text-emerald-400 font-medium">
              {verificationPayload.all_citations_valid ? "100% Grounded" : "Invalid Citations Flagged"}
            </span>
          </div>
          <div className="text-slate-400 font-mono text-[11px]">
            Completeness Gate:{" "}
            <span className="text-emerald-400 font-semibold">
              {verificationPayload.completeness_threshold_passed ? "PASSED" : "FAILED"}
            </span>
          </div>
        </div>
      )}

      {/* Critic's Audit Commentary */}
      <div className="space-y-1.5">
        <h4 className="text-xs uppercase tracking-wider font-semibold text-slate-400">
          Critical Evaluation & Skeptical Audit
        </h4>
        <p className="text-sm text-slate-300 leading-relaxed p-3.5 rounded-lg bg-slate-950/80 border border-slate-800/80">
          {criticPayload.critique}
        </p>
      </div>

      {/* Cognitive Biases Flagged */}
      {criticPayload.identified_cognitive_biases.length > 0 && (
        <div className="p-3.5 rounded-lg bg-rose-950/20 border border-rose-900/40 space-y-1.5">
          <h4 className="text-xs font-semibold text-rose-400 flex items-center gap-1.5">
            <AlertOctagon className="w-3.5 h-3.5 text-rose-400" />
            Identified Cognitive Fallacies / Confounder Gaps
          </h4>
          <ul className="list-disc list-inside space-y-0.5 text-xs text-rose-200/90 pl-1">
            {criticPayload.identified_cognitive_biases.map((bias, i) => (
              <li key={i}>{bias}</li>
            ))}
          </ul>
        </div>
      )}

      {/* Overruled Action & Rationale */}
      <div className="pt-2 border-t border-slate-800 space-y-2">
        <div className="flex items-center justify-between">
          <span className="text-xs text-slate-400 font-medium">Audited Clinical Action:</span>
          {criticPayload.overruled_action ? (
            <ClinicalActionBadge action={criticPayload.overruled_action} size="sm" />
          ) : (
            <span className="text-xs font-mono text-emerald-400">Maintained as Prescribed</span>
          )}
        </div>
        <p className="text-xs text-slate-400 leading-normal">
          <strong className="text-slate-300">Clinical Rationale:</strong> {criticPayload.action_rationale}
        </p>
      </div>
    </div>
  );
};
