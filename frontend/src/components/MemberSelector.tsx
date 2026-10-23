import React from "react";
import { MemberSummary } from "../lib/types";
import { User, CheckCircle2, AlertTriangle, AlertCircle, Plus, Trash2, Filter } from "lucide-react";

interface Props {
  members: MemberSummary[];
  selectedId: string;
  onSelect: (id: string) => void;
  loading: boolean;
  onAddMemberClick: () => void;
  onDeleteMember?: (id: string) => void;
  selectedCohort: string;
  onSelectCohort: (cohort: string) => void;
  cohorts: string[];
}

export const MemberSelector: React.FC<Props> = ({
  members,
  selectedId,
  onSelect,
  loading,
  onAddMemberClick,
  onDeleteMember,
  selectedCohort,
  onSelectCohort,
  cohorts,
}) => {
  const getPersonaBadge = (id: string) => {
    switch (id) {
      case "MEM-1001":
        return {
          label: "Clean Benchmark",
          color: "bg-emerald-500/10 text-emerald-400 border-emerald-500/30",
          icon: CheckCircle2,
        };
      case "MEM-1002":
        return {
          label: "Confounded Benchmark",
          color: "bg-amber-500/10 text-amber-400 border-amber-500/30",
          icon: AlertCircle,
        };
      case "MEM-1003":
        return {
          label: "Sparse Benchmark",
          color: "bg-purple-500/10 text-purple-400 border-purple-500/30",
          icon: AlertTriangle,
        };
      default:
        return {
          label: "Custom Test Case",
          color: "bg-sky-500/10 text-sky-400 border-sky-500/30",
          icon: User,
        };
    }
  };

  const isProtectedPersona = (id: string) => {
    return ["MEM-1001", "MEM-1002", "MEM-1003"].includes(id);
  };

  const filteredMembers = selectedCohort === "All"
    ? members
    : members.filter((m) => m.cohort === selectedCohort);

  return (
    <div className="space-y-4">
      {/* Top Bar: Cohort filter pills and Add Member Button */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-1">
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0 scrollbar-none text-xs">
          <div className="flex items-center gap-1 text-slate-500 mr-1 font-medium">
            <Filter className="w-3.5 h-3.5" />
            <span>Cohort:</span>
          </div>
          {cohorts.map((cohort) => (
            <button
              key={cohort}
              onClick={() => onSelectCohort(cohort)}
              className={`px-3 py-1 rounded-full text-xs font-medium whitespace-nowrap transition-all ${
                selectedCohort === cohort
                  ? "bg-sky-500/20 text-sky-300 border border-sky-500/40"
                  : "bg-slate-900 border border-slate-800 text-slate-400 hover:text-slate-200 hover:border-slate-700"
              }`}
            >
              {cohort}
            </button>
          ))}
        </div>

        <button
          onClick={onAddMemberClick}
          className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 text-xs font-bold shadow-md shadow-sky-500/10 transition-all shrink-0 cursor-pointer"
        >
          <Plus className="w-3.5 h-3.5 stroke-[2.5]" />
          <span>Add Test Case User</span>
        </button>
      </div>

      {/* Members Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {filteredMembers.map((m) => {
          const isSelected = m.id === selectedId;
          const badge = getPersonaBadge(m.id);
          const Icon = badge.icon;
          const isDeletable = !isProtectedPersona(m.id) && onDeleteMember;

          return (
            <div
              key={m.id}
              onClick={() => onSelect(m.id)}
              className={`relative p-4 rounded-xl border text-left transition-all cursor-pointer ${
                isSelected
                  ? "bg-slate-900 border-sky-500 shadow-lg shadow-sky-500/10 ring-1 ring-sky-500"
                  : "bg-slate-900/50 border-slate-800 hover:border-slate-700 hover:bg-slate-900"
              }`}
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2.5">
                  <div
                    className={`w-9 h-9 rounded-lg flex items-center justify-center font-bold text-sm ${
                      isSelected ? "bg-sky-500 text-slate-950" : "bg-slate-800 text-slate-300"
                    }`}
                  >
                    {m.full_name
                      .split(" ")
                      .map((n) => n[0])
                      .join("")}
                  </div>
                  <div>
                    <h3 className="font-semibold text-white text-sm">{m.full_name}</h3>
                    <p className="text-xs text-slate-400">
                      {m.id} • {m.age}y {m.biological_sex}
                    </p>
                  </div>
                </div>

                <div className="flex items-center gap-1.5">
                  <span
                    className={`inline-flex items-center gap-1 text-[11px] px-2 py-0.5 rounded-full border ${badge.color}`}
                  >
                    <Icon className="w-3 h-3" />
                    {badge.label}
                  </span>

                  {isDeletable && (
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        if (confirm(`Delete custom test member ${m.full_name} (${m.id})?`)) {
                          onDeleteMember(m.id);
                        }
                      }}
                      title="Delete test member"
                      className="p-1 rounded text-slate-500 hover:text-rose-400 hover:bg-rose-500/10 transition-colors"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  )}
                </div>
              </div>

              {/* Cohort Pill */}
              <div className="mt-2">
                <span className="inline-block text-[10px] font-medium text-sky-300 bg-sky-950/60 border border-sky-800/40 px-2 py-0.5 rounded">
                  {m.cohort || "General Cohort"}
                </span>
              </div>

              <p className="text-xs text-slate-300 line-clamp-2 mt-2">
                <span className="text-slate-500 font-medium">Goal:</span> {m.primary_goal}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
};
