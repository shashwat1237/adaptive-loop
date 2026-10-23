import React from "react";
import { ActionRecommendation } from "../lib/types";
import { CheckCircle2, AlertCircle, Clock, AlertTriangle, HelpCircle } from "lucide-react";

interface Props {
  action: ActionRecommendation;
  size?: "sm" | "md" | "lg";
}

export const ClinicalActionBadge: React.FC<Props> = ({ action, size = "md" }) => {
  const config = {
    CONTINUE_PROTOCOL: {
      label: "Continue Protocol As Prescribed",
      bg: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
      icon: CheckCircle2,
    },
    EXTEND_OBSERVATION: {
      label: "Extend Observation Window",
      bg: "bg-sky-500/10 text-sky-400 border-sky-500/30",
      icon: Clock,
    },
    ADJUST_WITH_CLINICIAN: {
      label: "Adjust Protocol With Clinician",
      bg: "bg-amber-500/10 text-amber-400 border-amber-500/30",
      icon: AlertCircle,
    },
    CLINICAL_ESCALATION: {
      label: "Immediate Clinical Escalation",
      bg: "bg-rose-500/10 text-rose-400 border-rose-500/30",
      icon: AlertTriangle,
    },
    ABSTAIN_MORE_DATA_REQUIRED: {
      label: "Abstain / More Data Required",
      bg: "bg-purple-500/10 text-purple-400 border-purple-500/30",
      icon: HelpCircle,
    },
  }[action] || {
    label: action,
    bg: "bg-slate-500/10 text-slate-400 border-slate-500/30",
    icon: HelpCircle,
  };

  const Icon = config.icon;
  const sizeClasses = {
    sm: "px-2.5 py-0.5 text-xs gap-1.5",
    md: "px-3.5 py-1.5 text-sm gap-2",
    lg: "px-4 py-2 text-base gap-2.5",
  }[size];

  return (
    <span
      className={`inline-flex items-center font-medium rounded-full border ${config.bg} ${sizeClasses}`}
    >
      <Icon className={size === "sm" ? "w-3.5 h-3.5" : size === "md" ? "w-4 h-4" : "w-5 h-5"} />
      {config.label}
    </span>
  );
};
