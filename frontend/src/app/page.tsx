"use client";

import React, { useEffect, useState } from "react";
import { Navbar } from "../components/Navbar";
import { MemberSelector } from "../components/MemberSelector";
import { ProtocolSummary } from "../components/ProtocolSummary";
import { ConfounderTimeline } from "../components/ConfounderTimeline";
import { LongitudinalChart } from "../components/LongitudinalChart";
import { AnalystReportCard } from "../components/AnalystReportCard";
import { CriticAuditCard } from "../components/CriticAuditCard";
import { ClinicalActionBadge } from "../components/ClinicalActionBadge";
import { AddMemberModal } from "../components/AddMemberModal";
import {
  MemberSummary,
  MemberDetail,
  TimelineData,
  AnalysisRun,
  MemberCreateInput,
} from "../lib/types";
import {
  fetchMembers,
  fetchMemberDetail,
  fetchMemberTimeline,
  triggerAnalysis,
  createMember,
  deleteMember,
} from "../lib/api";
import {
  Play,
  RotateCw,
  Sparkles,
  AlertCircle,
  ShieldAlert,
  CheckCircle2,
  Cpu,
  Layers,
  ArrowRight,
  ShieldCheck,
  RefreshCw,
} from "lucide-react";

export default function DashboardPage() {
  const [members, setMembers] = useState<MemberSummary[]>([]);
  const [selectedMemberId, setSelectedMemberId] = useState<string>("MEM-1001");
  const [memberDetail, setMemberDetail] = useState<MemberDetail | null>(null);
  const [timelineData, setTimelineData] = useState<TimelineData | null>(null);
  const [analysisRun, setAnalysisRun] = useState<AnalysisRun | null>(null);

  const [selectedCohort, setSelectedCohort] = useState<string>("All");
  const [isAddModalOpen, setIsAddModalOpen] = useState<boolean>(false);

  const [loadingMembers, setLoadingMembers] = useState<boolean>(true);
  const [loadingData, setLoadingData] = useState<boolean>(false);
  const [runningAnalysis, setRunningAnalysis] = useState<boolean>(false);
  const [analysisStage, setAnalysisStage] = useState<string>("idle");
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Load members on mount
  useEffect(() => {
    async function init() {
      try {
        setLoadingMembers(true);
        const membersData = await fetchMembers();
        setMembers(membersData);
        if (membersData.length > 0) {
          setSelectedMemberId(membersData[0].id);
        }
      } catch (err: any) {
        setErrorMessage(err.message || "Failed to load members from backend API");
      } finally {
        setLoadingMembers(false);
      }
    }
    init();
  }, []);

  // Compute available cohorts list
  const cohorts = ["All", ...Array.from(new Set(members.map((m) => m.cohort).filter(Boolean)))];

  // Load details and timeline when selected member changes
  // NOTE: We deliberately do NOT fetch or store analysis results beforehand.
  // Results are only computed on-demand when the user clicks "Run Adaptive Analysis".
  useEffect(() => {
    if (!selectedMemberId) return;

    async function loadMemberContent() {
      try {
        setLoadingData(true);
        setErrorMessage(null);
        // Clear previous analysis run immediately when changing member so no results are shown beforehand
        setAnalysisRun(null);
        setAnalysisStage("idle");

        const [detail, timeline] = await Promise.all([
          fetchMemberDetail(selectedMemberId),
          fetchMemberTimeline(selectedMemberId),
        ]);
        setMemberDetail(detail);
        setTimelineData(timeline);
      } catch (err: any) {
        setErrorMessage(err.message || "Failed to load member telemetry");
      } finally {
        setLoadingData(false);
      }
    }
    loadMemberContent();
  }, [selectedMemberId]);

  // Trigger analysis execution on explicit user click
  const handleRunAnalysis = async (forceRecompute = true) => {
    if (!selectedMemberId) return;
    try {
      setRunningAnalysis(true);
      setErrorMessage(null);
      setAnalysisStage("Stage 1/4: Aggregating telemetry & computing deltas...");

      // Small UI simulation of neuro-symbolic stages while the live request executes
      const stageTimer1 = setTimeout(() => {
        setAnalysisStage("Stage 2/4: Live Groq LLM Analyst (openai/gpt-oss-120b) formulating clinical hypotheses...");
      }, 1000);

      const stageTimer2 = setTimeout(() => {
        setAnalysisStage("Stage 3/4: Deterministic Citation Checker auditing claims against database observation registry...");
      }, 3500);

      const stageTimer3 = setTimeout(() => {
        setAnalysisStage("Stage 4/4: Adversarial LLM Critic auditing safety, confounders & bias...");
      }, 5500);

      const res = await triggerAnalysis(selectedMemberId, forceRecompute);

      clearTimeout(stageTimer1);
      clearTimeout(stageTimer2);
      clearTimeout(stageTimer3);

      setAnalysisRun(res);
      setAnalysisStage("completed");
      setSuccessMessage(`Live Adaptive Loop analysis completed for ${memberDetail?.member.full_name || selectedMemberId}!`);

      // Refresh members list so has_completed_analysis reflects the newly run state
      fetchMembers().then(setMembers).catch(() => {});
    } catch (err: any) {
      setErrorMessage(err.message || "Analysis execution failed");
      setAnalysisStage("failed");
    } finally {
      setRunningAnalysis(false);
    }
  };

  // Create custom test member
  const handleCreateMember = async (input: MemberCreateInput) => {
    const created = await createMember(input);
    const updatedMembers = await fetchMembers();
    setMembers(updatedMembers);
    setSelectedMemberId(created.member.id);
    setSelectedCohort("All");
    setAnalysisRun(null);
    setSuccessMessage(`Test case member "${created.member.full_name}" created with cohort "${created.member.cohort}". Ready for analysis!`);
  };

  // Delete custom member
  const handleDeleteMember = async (memberId: string) => {
    try {
      await deleteMember(memberId);
      const updatedMembers = await fetchMembers();
      setMembers(updatedMembers);
      if (selectedMemberId === memberId && updatedMembers.length > 0) {
        setSelectedMemberId(updatedMembers[0].id);
      }
      setSuccessMessage(`Member ${memberId} was deleted.`);
    } catch (err: any) {
      setErrorMessage(err.message || "Failed to delete member");
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col text-slate-100">
      <Navbar />

      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        {/* Success notification */}
        {successMessage && (
          <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-emerald-300 text-sm flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <CheckCircle2 className="w-5 h-5 shrink-0 text-emerald-400" />
              <span>{successMessage}</span>
            </div>
            <button
              onClick={() => setSuccessMessage(null)}
              className="text-xs uppercase font-mono px-2 py-1 rounded bg-emerald-500/20 hover:bg-emerald-500/30"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Error banner */}
        {errorMessage && (
          <div className="p-4 rounded-xl bg-rose-500/10 border border-rose-500/30 text-rose-300 text-sm flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <AlertCircle className="w-5 h-5 shrink-0 text-rose-400" />
              <span>{errorMessage}</span>
            </div>
            <button
              onClick={() => setErrorMessage(null)}
              className="text-xs uppercase font-mono px-2 py-1 rounded bg-rose-500/20 hover:bg-rose-500/30"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Section 1: Member Persona & Cohort Selector */}
        <div>
          <div className="flex items-center justify-between mb-3">
            <div>
              <h2 className="text-base font-bold text-white tracking-tight">Clinical Cohorts & Member Personas</h2>
              <p className="text-xs text-slate-400">
                Select a test case member to load their longitudinal dataset. Analysis is computed on-demand upon clicking the analysis button.
              </p>
            </div>
          </div>
          <MemberSelector
            members={members}
            selectedId={selectedMemberId}
            onSelect={setSelectedMemberId}
            loading={loadingMembers || loadingData}
            onAddMemberClick={() => setIsAddModalOpen(true)}
            onDeleteMember={handleDeleteMember}
            selectedCohort={selectedCohort}
            onSelectCohort={setSelectedCohort}
            cohorts={cohorts}
          />
        </div>

        {/* Section 2: Active Member Profile & Analysis Action Bar */}
        {memberDetail && (
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div>
              <div className="flex flex-wrap items-center gap-2.5">
                <h2 className="text-lg font-bold text-white tracking-tight">
                  {memberDetail.member.full_name}
                </h2>
                <span className="text-xs font-mono px-2.5 py-0.5 rounded-full bg-slate-800 text-slate-300 border border-slate-700">
                  {memberDetail.member.id}
                </span>
                <span className="text-xs font-semibold px-2.5 py-0.5 rounded-full bg-sky-500/10 text-sky-400 border border-sky-500/30">
                  Cohort: {memberDetail.member.cohort || "General"}
                </span>
                <span className="text-xs text-slate-400">
                  {memberDetail.member.age} yrs • {memberDetail.member.biological_sex}
                </span>
              </div>
              <p className="text-xs text-slate-400 mt-1.5">
                <strong className="text-slate-300">Clinical Focus:</strong> {memberDetail.member.primary_goal}
              </p>
              {memberDetail.member.baseline_notes && (
                <p className="text-[11px] text-slate-500 mt-0.5 italic">
                  Notes: {memberDetail.member.baseline_notes}
                </p>
              )}
            </div>

            <div className="flex items-center gap-3 shrink-0">
              <button
                onClick={() => handleRunAnalysis(true)}
                disabled={runningAnalysis || loadingData}
                className="flex items-center gap-2.5 px-5 py-3 rounded-xl bg-gradient-to-r from-emerald-500 to-sky-600 hover:from-emerald-400 hover:to-sky-500 text-slate-950 font-bold text-sm shadow-xl shadow-emerald-500/20 transition-all disabled:opacity-50 disabled:cursor-not-allowed cursor-pointer"
              >
                {runningAnalysis ? (
                  <>
                    <RotateCw className="w-4 h-4 animate-spin" />
                    <span>Executing Live 4-Stage Loop...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-current" />
                    <span>Run Adaptive Analysis</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}

        {/* Section 3: Longitudinal Chart */}
        {timelineData && memberDetail && (
          <LongitudinalChart
            weeklyRollups={timelineData.weekly_rollups}
            confounders={timelineData.confounders}
            biomarkers={memberDetail.biomarkers}
          />
        )}

        {/* Section 4: Protocols & Confounders Grid */}
        {memberDetail && timelineData && (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <ProtocolSummary
              protocols={memberDetail.protocols}
              overallAdherence={timelineData.protocol_adherence_rate}
            />
            <ConfounderTimeline confounders={timelineData.confounders} />
          </div>
        )}

        {/* Section 5: Adaptive Loop Results or Pre-Execution CTA */}
        {runningAnalysis && (
          <div className="bg-slate-900 border border-sky-500/40 rounded-xl p-6 text-center space-y-3 shadow-xl shadow-sky-500/10">
            <div className="w-12 h-12 rounded-2xl bg-sky-500/10 border border-sky-500/30 flex items-center justify-center text-sky-400 mx-auto">
              <RotateCw className="w-6 h-6 animate-spin" />
            </div>
            <h3 className="text-base font-bold text-white tracking-tight">
              Executing Neuro-Symbolic Intelligence Engine
            </h3>
            <p className="text-xs text-sky-400 font-mono">
              {analysisStage}
            </p>
            <div className="max-w-md mx-auto pt-2">
              <div className="w-full bg-slate-800 rounded-full h-1.5 overflow-hidden">
                <div className="bg-gradient-to-r from-sky-500 to-emerald-400 h-1.5 rounded-full animate-pulse w-3/4" />
              </div>
            </div>
          </div>
        )}

        {!runningAnalysis && !analysisRun && memberDetail && (
          <div className="bg-slate-900/60 border border-dashed border-slate-800 rounded-xl p-8 text-center space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-slate-800/80 border border-slate-700/60 flex items-center justify-center text-slate-400 mx-auto">
              <Cpu className="w-6 h-6 text-sky-400" />
            </div>
            <div className="max-w-lg mx-auto space-y-1">
              <h3 className="text-base font-semibold text-white">
                No Pre-Calculated Results Loaded
              </h3>
              <p className="text-xs text-slate-400">
                Patient telemetry for <span className="text-slate-200 font-medium">{memberDetail.member.full_name}</span> is staged. Click the button below to initiate real-time inference using Groq’s <span className="text-sky-400 font-mono">openai/gpt-oss-120b</span> and deterministic citation verification.
              </p>
            </div>
            <button
              onClick={() => handleRunAnalysis(true)}
              disabled={loadingData}
              className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-sky-500 hover:bg-sky-400 text-slate-950 font-bold text-xs shadow-lg shadow-sky-500/20 transition-all cursor-pointer"
            >
              <Play className="w-3.5 h-3.5 fill-current" />
              <span>Trigger Live Intervention Analysis</span>
            </button>
          </div>
        )}

        {!runningAnalysis && analysisRun && (
          <div className="space-y-6 pt-4 border-t border-slate-800/80">
            {/* Header with Canonical Action Badge and Re-run option */}
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-slate-900 border border-slate-800 rounded-xl p-5">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs uppercase font-mono tracking-wider text-slate-400 font-semibold">
                    Cycle Result
                  </span>
                  <span className="text-xs font-mono text-slate-500">• {analysisRun.id}</span>
                </div>
                <h3 className="text-base font-bold text-white mt-1">
                  Synthesized Clinical Recommendation
                </h3>
              </div>

              <div className="flex items-center gap-3">
                <ClinicalActionBadge action={analysisRun.final_action} size="lg" />
                <button
                  onClick={() => setAnalysisRun(null)}
                  title="Clear result to test again"
                  className="p-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white transition-colors text-xs flex items-center gap-1.5"
                >
                  <RefreshCw className="w-3.5 h-3.5" />
                  <span>Reset</span>
                </button>
              </div>
            </div>

            {/* Invariant & Abstention Warning if applicable */}
            {(analysisRun.status === "ABSTAINED" || analysisRun.final_action === "ABSTAIN_MORE_DATA_REQUIRED") && (
              <div className="p-4 rounded-xl bg-purple-500/10 border border-purple-500/30 text-purple-300 text-sm flex items-start gap-3">
                <ShieldAlert className="w-5 h-5 text-purple-400 shrink-0 mt-0.5" />
                <div>
                  <h4 className="font-semibold text-white">Principled Abstention Triggered</h4>
                  <p className="text-xs text-purple-300 mt-1">
                    The engine detected insufficient data completeness ({analysisRun.data_completeness_rate}%) or low protocol adherence ({analysisRun.protocol_adherence_rate}%). As strictly mandated by clinical safety rules, inference was halted early without fabricating hypotheses.
                  </p>
                </div>
              </div>
            )}

            {/* Analyst & Critic Dual-Audit Cards */}
            {analysisRun.status === "COMPLETED" && (
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {analysisRun.analyst_payload && (
                  <AnalystReportCard
                    analystPayload={analysisRun.analyst_payload}
                  />
                )}
                {analysisRun.critic_payload && (
                  <CriticAuditCard
                    criticPayload={analysisRun.critic_payload}
                    verificationPayload={analysisRun.verification_payload}
                  />
                )}
              </div>
            )}
          </div>
        )}
      </main>

      {/* Add Custom Member & Cohort Modal */}
      <AddMemberModal
        isOpen={isAddModalOpen}
        onClose={() => setIsAddModalOpen(false)}
        onSubmit={handleCreateMember}
      />
    </div>
  );
}
