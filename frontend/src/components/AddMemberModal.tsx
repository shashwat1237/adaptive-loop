"use client";

import React, { useState } from "react";
import { MemberCreateInput, BiologicalSex, ProtocolCategory, ConfounderEventType, ConfounderSeverity } from "../lib/types";
import { X, Plus, Sparkles, Activity, ShieldCheck, HeartPulse, UserPlus, Info } from "lucide-react";

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (input: MemberCreateInput) => Promise<void>;
}

const PRESET_COHORTS = [
  "Cardiometabolic & Longevity",
  "Neuro-Endocrine & Sleep Architecture",
  "Metabolic Syndrome & Glycemic Control",
  "Cellular Longevity & NAD+ Recovery",
  "Executive Stress & Autonomic Recovery",
  "Custom Cohort"
];

export const AddMemberModal: React.FC<Props> = ({ isOpen, onClose, onSubmit }) => {
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [fullName, setFullName] = useState("");
  const [age, setAge] = useState(42);
  const [biologicalSex, setBiologicalSex] = useState<BiologicalSex>("FEMALE");
  const [selectedCohortPreset, setSelectedCohortPreset] = useState("Cardiometabolic & Longevity");
  const [customCohort, setCustomCohort] = useState("");
  const [primaryGoal, setPrimaryGoal] = useState("ApoB reduction & autonomic HRV restoration");
  const [baselineNotes, setBaselineNotes] = useState("Active corporate professional with elevated cardiovascular risk markers.");

  // Protocol state
  const [protocolName, setProtocolName] = useState("Zone 2 Aerobic Base + Citrus Bergamot");
  const [protocolCategory, setProtocolCategory] = useState<ProtocolCategory>("SUPPLEMENT");
  const [dosage, setDosage] = useState("500 mg daily with evening meal");
  const [targetAdherence, setTargetAdherence] = useState(85.0);

  // Biomarkers state
  const [marker1Code, setMarker1Code] = useState("APOB");
  const [marker1Name, setMarker1Name] = useState("Apolipoprotein B");
  const [marker1Base, setMarker1Base] = useState(128.0);
  const [marker1Follow, setMarker1Follow] = useState(101.0);
  const [marker1Unit, setMarker1Unit] = useState("mg/dL");

  const [marker2Code, setMarker2Code] = useState("CRP");
  const [marker2Name, setMarker2Name] = useState("High-Sensitivity CRP");
  const [marker2Base, setMarker2Base] = useState(2.6);
  const [marker2Follow, setMarker2Follow] = useState(1.2);
  const [marker2Unit, setMarker2Unit] = useState("mg/L");

  // Telemetry profile
  const [telemetryProfile, setTelemetryProfile] = useState<"clean_responder" | "confounded_responder" | "non_adherent" | "custom">("clean_responder");
  const [baselineRhr, setBaselineRhr] = useState(68.0);
  const [baselineHrv, setBaselineHrv] = useState(36.0);
  const [baselineDeep, setBaselineDeep] = useState(1.1);
  const [followupRhr, setFollowupRhr] = useState(62.0);
  const [followupHrv, setFollowupHrv] = useState(48.0);
  const [followupDeep, setFollowupDeep] = useState(1.6);

  // Confounders state
  const [includeConfounder, setIncludeConfounder] = useState(false);
  const [confounderType, setConfounderType] = useState<ConfounderEventType>("ILLNESS");
  const [confounderDesc, setConfounderDesc] = useState("Acute upper respiratory infection with temporary fever");
  const [confounderWeek, setConfounderWeek] = useState(8);
  const [confounderDuration, setConfounderDuration] = useState(14);
  const [confounderSeverity, setConfounderSeverity] = useState<ConfounderSeverity>("MODERATE");

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (!fullName.trim()) {
      setError("Please enter a member name.");
      return;
    }

    const cohort = selectedCohortPreset === "Custom Cohort" ? customCohort.trim() || "Custom Cohort" : selectedCohortPreset;

    const input: MemberCreateInput = {
      full_name: fullName.trim(),
      age: Number(age),
      biological_sex: biologicalSex,
      cohort: cohort,
      primary_goal: primaryGoal.trim(),
      baseline_notes: baselineNotes.trim() || undefined,
      telemetry_profile: telemetryProfile,
      baseline_resting_hr: Number(baselineRhr),
      baseline_hrv_rmssd: Number(baselineHrv),
      baseline_deep_sleep_hours: Number(baselineDeep),
      baseline_total_sleep_hours: 6.8,
      followup_resting_hr: Number(followupRhr),
      followup_hrv_rmssd: Number(followupHrv),
      followup_deep_sleep_hours: Number(followupDeep),
      followup_total_sleep_hours: 7.4,
      protocols: [
        {
          name: protocolName.trim(),
          category: protocolCategory,
          dosage_or_frequency: dosage.trim(),
          target_adherence_rate: Number(targetAdherence),
        },
      ],
      biomarkers: [
        {
          marker_code: marker1Code.trim().toUpperCase(),
          marker_name: marker1Name.trim(),
          baseline_value: Number(marker1Base),
          followup_value: Number(marker1Follow),
          unit: marker1Unit.trim(),
          optimal_range_min: 40.0,
          optimal_range_max: 80.0,
        },
        {
          marker_code: marker2Code.trim().toUpperCase(),
          marker_name: marker2Name.trim(),
          baseline_value: Number(marker2Base),
          followup_value: Number(marker2Follow),
          unit: marker2Unit.trim(),
          optimal_range_min: 0.0,
          optimal_range_max: 1.0,
        },
      ],
      confounders: includeConfounder || telemetryProfile === "confounded_responder"
        ? [
            {
              event_type: confounderType,
              description: confounderDesc.trim(),
              start_week: Number(confounderWeek),
              duration_days: Number(confounderDuration),
              severity: confounderSeverity,
            },
          ]
        : undefined,
    };

    try {
      setSubmitting(true);
      await onSubmit(input);
      onClose();
    } catch (err: any) {
      setError(err.message || "Failed to create test member");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/80 backdrop-blur-sm overflow-y-auto">
      <div className="relative w-full max-w-3xl bg-slate-900 border border-slate-800 rounded-2xl shadow-2xl p-6 sm:p-8 my-8 text-slate-100 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400">
              <UserPlus className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-lg font-bold text-white tracking-tight">Create Custom Test Case Member & Cohort</h2>
              <p className="text-xs text-slate-400">
                Configure patient demographics, cohort classification, protocols, and 180-day telemetry
              </p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {error && (
          <div className="mt-4 p-3 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-xs">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit} className="mt-6 space-y-6 text-xs">
          {/* Section 1: Demographics & Cohort */}
          <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/80 space-y-4">
            <h3 className="text-sm font-semibold text-sky-400 flex items-center gap-2">
              <ShieldCheck className="w-4 h-4" /> 1. Member Profile & Cohort Grouping
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="sm:col-span-2">
                <label className="block text-slate-400 font-medium mb-1">Full Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Dr. Julian Croft"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                />
              </div>

              <div>
                <label className="block text-slate-400 font-medium mb-1">Age</label>
                <input
                  type="number"
                  min={18}
                  max={120}
                  value={age}
                  onChange={(e) => setAge(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 font-medium mb-1">Biological Sex</label>
                <select
                  value={biologicalSex}
                  onChange={(e) => setBiologicalSex(e.target.value as BiologicalSex)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500"
                >
                  <option value="FEMALE">FEMALE</option>
                  <option value="MALE">MALE</option>
                  <option value="OTHER">OTHER</option>
                </select>
              </div>

              <div>
                <label className="block text-slate-400 font-medium mb-1">Target Cohort</label>
                <select
                  value={selectedCohortPreset}
                  onChange={(e) => setSelectedCohortPreset(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500"
                >
                  {PRESET_COHORTS.map((c) => (
                    <option key={c} value={c}>{c}</option>
                  ))}
                </select>
              </div>
            </div>

            {selectedCohortPreset === "Custom Cohort" && (
              <div>
                <label className="block text-slate-400 font-medium mb-1">Custom Cohort Name</label>
                <input
                  type="text"
                  placeholder="e.g. Cognitive Resilience & Amyloid Clearance"
                  value={customCohort}
                  onChange={(e) => setCustomCohort(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white placeholder-slate-500 focus:outline-none focus:border-sky-500"
                />
              </div>
            )}

            <div>
              <label className="block text-slate-400 font-medium mb-1">Primary Clinical Health Goal</label>
              <input
                type="text"
                required
                value={primaryGoal}
                onChange={(e) => setPrimaryGoal(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500"
              />
            </div>

            <div>
              <label className="block text-slate-400 font-medium mb-1">Baseline Clinical Notes</label>
              <textarea
                rows={2}
                value={baselineNotes}
                onChange={(e) => setBaselineNotes(e.target.value)}
                className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-sky-500"
              />
            </div>
          </div>

          {/* Section 2: Intervention Protocol */}
          <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/80 space-y-4">
            <h3 className="text-sm font-semibold text-emerald-400 flex items-center gap-2">
              <Sparkles className="w-4 h-4" /> 2. Prescribed Protocol
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 font-medium mb-1">Protocol Name</label>
                <input
                  type="text"
                  required
                  value={protocolName}
                  onChange={(e) => setProtocolName(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-slate-400 font-medium mb-1">Category</label>
                <select
                  value={protocolCategory}
                  onChange={(e) => setProtocolCategory(e.target.value as ProtocolCategory)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                >
                  <option value="SUPPLEMENT">SUPPLEMENT</option>
                  <option value="EXERCISE">EXERCISE</option>
                  <option value="LIFESTYLE">LIFESTYLE</option>
                  <option value="NUTRITION">NUTRITION</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-slate-400 font-medium mb-1">Dosage or Frequency</label>
                <input
                  type="text"
                  required
                  value={dosage}
                  onChange={(e) => setDosage(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>

              <div>
                <label className="block text-slate-400 font-medium mb-1">Target Adherence Rate (%)</label>
                <input
                  type="number"
                  min={10}
                  max={100}
                  value={targetAdherence}
                  onChange={(e) => setTargetAdherence(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-white focus:outline-none focus:border-emerald-500"
                />
              </div>
            </div>
          </div>

          {/* Section 3: Biomarker Measurements (Day 0 vs Day 180) */}
          <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/80 space-y-4">
            <h3 className="text-sm font-semibold text-purple-400 flex items-center gap-2">
              <Activity className="w-4 h-4" /> 3. Longitudinal Biomarkers (Day 0 Baseline vs Day 180 Follow-up)
            </h3>

            <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <div>
                <label className="block text-slate-400 font-medium mb-1">Marker Code</label>
                <input
                  type="text"
                  value={marker1Code}
                  onChange={(e) => setMarker1Code(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Baseline (D0)</label>
                <input
                  type="number"
                  step="0.1"
                  value={marker1Base}
                  onChange={(e) => setMarker1Base(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Follow-up (D180)</label>
                <input
                  type="number"
                  step="0.1"
                  value={marker1Follow}
                  onChange={(e) => setMarker1Follow(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Unit</label>
                <input
                  type="text"
                  value={marker1Unit}
                  onChange={(e) => setMarker1Unit(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-4 gap-3 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
              <div>
                <label className="block text-slate-400 font-medium mb-1">Marker Code</label>
                <input
                  type="text"
                  value={marker2Code}
                  onChange={(e) => setMarker2Code(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Baseline (D0)</label>
                <input
                  type="number"
                  step="0.1"
                  value={marker2Base}
                  onChange={(e) => setMarker2Base(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Follow-up (D180)</label>
                <input
                  type="number"
                  step="0.1"
                  value={marker2Follow}
                  onChange={(e) => setMarker2Follow(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Unit</label>
                <input
                  type="text"
                  value={marker2Unit}
                  onChange={(e) => setMarker2Unit(e.target.value)}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
            </div>
          </div>

          {/* Section 4: Wearable Telemetry & Confounder Simulation */}
          <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/80 space-y-4">
            <h3 className="text-sm font-semibold text-amber-400 flex items-center gap-2">
              <HeartPulse className="w-4 h-4" /> 4. 180-Day Telemetry Profile & Confounder Dynamics
            </h3>

            <div>
              <label className="block text-slate-400 font-medium mb-1">Telemetry Response Behavior</label>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <button
                  type="button"
                  onClick={() => setTelemetryProfile("clean_responder")}
                  className={`p-3 rounded-lg border text-left transition-all ${
                    telemetryProfile === "clean_responder"
                      ? "bg-emerald-950/50 border-emerald-500 text-white"
                      : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <p className="font-semibold text-emerald-400 text-xs">Clean Responder</p>
                  <p className="text-[10px] text-slate-400 mt-1">High completeness (&gt;90%), clear physiological recovery</p>
                </button>

                <button
                  type="button"
                  onClick={() => {
                    setTelemetryProfile("confounded_responder");
                    setIncludeConfounder(true);
                  }}
                  className={`p-3 rounded-lg border text-left transition-all ${
                    telemetryProfile === "confounded_responder"
                      ? "bg-amber-950/50 border-amber-500 text-white"
                      : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <p className="font-semibold text-amber-400 text-xs">Confounded Case</p>
                  <p className="text-[10px] text-slate-400 mt-1">Acute confounder dip in Week 8 testing Critic attribution</p>
                </button>

                <button
                  type="button"
                  onClick={() => setTelemetryProfile("non_adherent")}
                  className={`p-3 rounded-lg border text-left transition-all ${
                    telemetryProfile === "non_adherent"
                      ? "bg-purple-950/50 border-purple-500 text-white"
                      : "bg-slate-900 border-slate-800 text-slate-400 hover:border-slate-700"
                  }`}
                >
                  <p className="font-semibold text-purple-400 text-xs">Sparse Telemetry (&lt;50%)</p>
                  <p className="text-[10px] text-slate-400 mt-1">Triggers engine's deterministic abstention safety guard</p>
                </button>
              </div>
            </div>

            {/* Wearable metric baselines */}
            <div className="grid grid-cols-3 gap-3 pt-2">
              <div>
                <label className="block text-slate-400 font-medium mb-1">Baseline RHR (bpm)</label>
                <input
                  type="number"
                  value={baselineRhr}
                  onChange={(e) => setBaselineRhr(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Baseline HRV (ms)</label>
                <input
                  type="number"
                  value={baselineHrv}
                  onChange={(e) => setBaselineHrv(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
              <div>
                <label className="block text-slate-400 font-medium mb-1">Baseline Deep Sleep (h)</label>
                <input
                  type="number"
                  step="0.1"
                  value={baselineDeep}
                  onChange={(e) => setBaselineDeep(Number(e.target.value))}
                  className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                />
              </div>
            </div>

            {/* Confounder section */}
            <div className="pt-2 border-t border-slate-800/80">
              <label className="flex items-center gap-2 cursor-pointer mb-2">
                <input
                  type="checkbox"
                  checked={includeConfounder || telemetryProfile === "confounded_responder"}
                  onChange={(e) => setIncludeConfounder(e.target.checked)}
                  className="rounded border-slate-700 bg-slate-900 text-sky-500"
                />
                <span className="text-slate-300 font-medium">Inject Confounder Event</span>
              </label>

              {(includeConfounder || telemetryProfile === "confounded_responder") && (
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 bg-slate-900/60 p-3 rounded-lg border border-slate-800">
                  <div>
                    <label className="block text-slate-400 font-medium mb-1">Event Type</label>
                    <select
                      value={confounderType}
                      onChange={(e) => setConfounderType(e.target.value as ConfounderEventType)}
                      className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                    >
                      <option value="ILLNESS">ILLNESS</option>
                      <option value="TRAVEL">TRAVEL</option>
                      <option value="LIFE_STRESS">LIFE_STRESS</option>
                      <option value="INJURY">INJURY</option>
                    </select>
                  </div>
                  <div>
                    <label className="block text-slate-400 font-medium mb-1">Start Week (1-26)</label>
                    <input
                      type="number"
                      min={1}
                      max={24}
                      value={confounderWeek}
                      onChange={(e) => setConfounderWeek(Number(e.target.value))}
                      className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                    />
                  </div>
                  <div>
                    <label className="block text-slate-400 font-medium mb-1">Severity</label>
                    <select
                      value={confounderSeverity}
                      onChange={(e) => setConfounderSeverity(e.target.value as ConfounderSeverity)}
                      className="w-full bg-slate-900 border border-slate-700 rounded px-2 py-1.5 text-white"
                    >
                      <option value="MILD">MILD</option>
                      <option value="MODERATE">MODERATE</option>
                      <option value="SEVERE">SEVERE</option>
                    </select>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Footer Action Buttons */}
          <div className="flex items-center justify-end gap-3 pt-4 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              disabled={submitting}
              className="px-4 py-2 rounded-xl text-slate-400 hover:text-white hover:bg-slate-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={submitting}
              className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold shadow-lg shadow-sky-500/20 transition-all disabled:opacity-50"
            >
              {submitting ? (
                <>
                  <div className="w-4 h-4 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" />
                  <span>Synthesizing Telemetry...</span>
                </>
              ) : (
                <>
                  <Plus className="w-4 h-4" />
                  <span>Add Member to Database</span>
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
