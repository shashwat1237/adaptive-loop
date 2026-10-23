import json
from typing import Dict, Any, List
from app.models.member import Member
from app.models.protocol import Protocol
from app.schemas.analyst import AnalystPayloadSchema
from app.engine.llm_client import llm_client

ANALYST_SYSTEM_PROMPT = """You are the Intervention Intelligence Analyst, an advanced clinical reasoning system for longevity medicine.
Your role is to analyze a member's 180-day health protocol evaluation dataset.

CRITICAL INSTRUCTIONS:
1. You must NEVER diagnose medical diseases or alter prescription drug regimens.
2. Formulate at least ONE primary hypothesis connecting the protocol to observed outcomes, and at least ONE competing alternative explanation (e.g., confounders, lifestyle shifts, natural regression).
3. Every factual statement or physiological trend MUST explicitly cite one or more observation IDs from the provided registry.
4. Do NOT calculate arithmetic mentally; use the exact percentage deltas and rolling means provided in the context.
5. Provide your output strictly in valid JSON adhering to the specified schema. You MUST include ALL four top-level keys ('primary_hypothesis', 'competing_hypotheses', 'unresolved_uncertainties', 'initial_action_recommendation'):
{
  "primary_hypothesis": {
    "statement": "...",
    "confidence": "HIGH" | "MODERATE" | "LOW" | "INCONCLUSIVE",
    "cited_observations": ["OBS-BIO-...", "OBS-WEAR-..."]
  },
  "competing_hypotheses": [
    {
      "statement": "...",
      "confidence": "HIGH" | "MODERATE" | "LOW" | "INCONCLUSIVE",
      "cited_observations": ["..."]
    }
  ],
  "unresolved_uncertainties": ["..."],
  "initial_action_recommendation": "CONTINUE_PROTOCOL" | "EXTEND_OBSERVATION" | "ADJUST_WITH_CLINICIAN" | "CLINICAL_ESCALATION" | "ABSTAIN_MORE_DATA_REQUIRED"
}"""


class AIAnalyst:
    @staticmethod
    def generate_analysis(
        member: Member,
        protocols: List[Protocol],
        aggregated_data: Dict[str, Any]
    ) -> AnalystPayloadSchema:
        """Invokes the AI Analyst with token-optimized structured longitudinal context."""
        protocols_summary = "\n".join([
            f"- {p.name} ({p.category}): {p.dosage_or_frequency} [Target: {p.target_adherence_rate}%]"
            for p in protocols
        ])

        # Compact representation of deltas
        deltas_summary = "\n".join([
            f"- {b['marker_name']} ({b['marker_code']}): Baseline {b['baseline']} -> Follow-up {b['follow_up']} {b['unit']} (Delta: {b['delta_percentage']}%) [Optimal: {b['optimal_range_min']}-{b['optimal_range_max']}]"
            for b in aggregated_data.get("biomarker_deltas", [])
        ])

        # Compact representation of weekly rollups (key baseline, inflection, and endpoint weeks)
        weekly_rollups = aggregated_data.get("weekly_rollups", [])
        confounder_weeks = {c.get("start_week") for c in aggregated_data.get("confounders", []) if c.get("start_week")}
        key_weeks = {1, 4, 8, 12, 16, 20, 24, 26} | confounder_weeks
        
        compact_weeks = []
        for wr in weekly_rollups:
            w = wr["week_number"]
            if w in key_weeks or w == len(weekly_rollups):
                compact_weeks.append(
                    f"W{w:02d}: Sleep={wr.get('avg_total_sleep_hours')}h (Deep={wr.get('avg_deep_sleep_hours')}h), HRV={wr.get('avg_hrv_rmssd')}ms, RHR={wr.get('avg_resting_heart_rate')}bpm, Adh={wr.get('adherence_rate')}%"
                )
        weeks_summary = "\n".join(compact_weeks)

        # Compact confounders
        confounders = aggregated_data.get("confounders", [])
        confounders_summary = "\n".join([
            f"- {c['id']}: {c['event_type']} ({c['severity']}): {c['description']} [{c['start_date']} to {c['end_date']}]"
            for c in confounders
        ]) or "None recorded."

        # Filter registry keys to high-value citation targets to stay lean
        all_keys = list(aggregated_data.get("observation_registry", {}).keys())
        key_citations = [
            k for k in all_keys
            if k.startswith("OBS-BIO-") or k.startswith("CONF-") or any(f"-W{w:02d}" in k for w in key_weeks)
        ]

        user_prompt = f"""MEMBER CONTEXT:
ID: {member.id} | Name: {member.full_name} | Age: {member.age} | Sex: {member.biological_sex} | Goal: {member.primary_goal}
Baseline Notes: {member.baseline_notes or 'None'}

PRESCRIBED PROTOCOLS:
{protocols_summary}

DATA COMPLETENESS & ADHERENCE:
Completeness: {aggregated_data.get('data_completeness_rate')}% | Overall Adherence: {aggregated_data.get('protocol_adherence_rate')}%

BIOMARKER DELTAS:
{deltas_summary}

KEY WEARABLE INFLECTION POINTS:
{weeks_summary}

CONFOUNDER EVENTS:
{confounders_summary}

VALID OBSERVATION IDs FOR CITATIONS:
{', '.join(key_citations)}

Analyze this longitudinal profile and emit concise JSON adhering strictly to the schema with all 4 required keys."""

        raw_json = llm_client.call_chat_completion(
            system_prompt=ANALYST_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            member_id=member.id,
            stage="analyst"
        )

        return AnalystPayloadSchema(**raw_json)
