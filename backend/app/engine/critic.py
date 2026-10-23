import json
from typing import Dict, Any
from app.schemas.analyst import AnalystPayloadSchema
from app.schemas.critic import CriticPayloadSchema, VerificationPayloadSchema
from app.engine.llm_client import llm_client

CRITIC_SYSTEM_PROMPT = """You are the Clinical Adversarial Auditor and Chief Medical Critic.
Your role is to rigorously challenge, stress-test, and audit the AI Analyst's findings before they reach a clinician.

EVALUATION CRITERIA:
1. Attribution Fallacy Check: Did the Analyst falsely attribute an improvement to a supplement or lifestyle protocol when a major confounding event (e.g., job change, illness, travel) is a stronger explanation?
2. Citation Grounding: Check the attached Deterministic Verification Report. If any citations are invalid or calculations mismatched, penalize the analysis.
3. Overconfidence Penalty: If data completeness is low (<80%) or adherence is moderate, ensure the confidence is appropriately tempered.
4. Verdict Decision:
   - "APPROVED": The reasoning is cautious, grounded, and accounts for all data.
   - "AMENDED": The reasoning is plausible, but the action or confidence must be downgraded due to unaddressed confounders.
   - "REJECTED": The reasoning commits serious causal fallacies, cites fabricated data, or ignores critical health red flags.

Output format strictly JSON:
{
  "verdict": "APPROVED" | "AMENDED" | "REJECTED",
  "critique": "...",
  "identified_cognitive_biases": ["..."],
  "overruled_action": null | "CONTINUE_PROTOCOL" | "EXTEND_OBSERVATION" | "ADJUST_WITH_CLINICIAN" | "CLINICAL_ESCALATION" | "ABSTAIN_MORE_DATA_REQUIRED",
  "action_rationale": "..."
}"""


class AICritic:
    @staticmethod
    def audit_analysis(
        member_id: str,
        analyst_payload: AnalystPayloadSchema,
        aggregated_data: Dict[str, Any],
        verification_result: VerificationPayloadSchema
    ) -> CriticPayloadSchema:
        """Invokes the AI Critic with compact context and verification findings."""
        deltas = [
            f"{b['marker_code']}: {b['delta_percentage']}%"
            for b in aggregated_data.get("biomarker_deltas", [])
        ]
        confounders = [
            f"{c['id']} ({c['event_type']}): {c['description']}"
            for c in aggregated_data.get("confounders", [])
        ]

        user_prompt = f"""MEMBER: {member_id}
Completeness: {aggregated_data.get('data_completeness_rate')}% | Adherence: {aggregated_data.get('protocol_adherence_rate')}%
Deltas: {', '.join(deltas)}
Confounders: {'; '.join(confounders) or 'None'}

AI ANALYST OUTPUT TO AUDIT:
{analyst_payload.model_dump_json(indent=2)}

DETERMINISTIC VERIFICATION REPORT:
All Citations Valid: {verification_result.all_citations_valid}
Invalid Citations: {verification_result.invalid_citations}
Math Discrepancies: {verification_result.math_discrepancies}
Completeness Threshold Passed: {verification_result.completeness_threshold_passed}

Audit the Analyst's output and emit your verdict and critique in JSON."""

        raw_json = llm_client.call_chat_completion(
            system_prompt=CRITIC_SYSTEM_PROMPT,
            user_prompt=user_prompt,
            member_id=member_id,
            stage="critic"
        )

        return CriticPayloadSchema(**raw_json)
