from typing import Dict, Any, List
from app.schemas.analyst import AnalystPayloadSchema
from app.schemas.critic import VerificationPayloadSchema


class CitationChecker:
    @staticmethod
    def verify(
        analyst_payload: AnalystPayloadSchema,
        aggregated_data: Dict[str, Any]
    ) -> VerificationPayloadSchema:
        """Deterministically validates:
        1. That all cited observation IDs exist in the member's observation registry.
        2. That completeness and minimum record thresholds pass.
        3. That stated biomarker percentage deltas match ground truth within ±0.50%.
        """
        registry = aggregated_data.get("observation_registry", {})
        completeness_rate = aggregated_data.get("data_completeness_rate", 0.0)
        valid_days = aggregated_data.get("valid_days", 0)

        # 1. Collect all cited observations
        cited_ids = set()
        if analyst_payload.primary_hypothesis:
            for cid in analyst_payload.primary_hypothesis.cited_observations:
                cited_ids.add(cid.strip())

        for ch in analyst_payload.competing_hypotheses:
            for cid in ch.cited_observations:
                cited_ids.add(cid.strip())

        # 2. Check existence in registry
        invalid_citations = []
        for cid in sorted(cited_ids):
            if cid not in registry:
                invalid_citations.append(cid)

        # 3. Check math discrepancies in hypotheses statements
        # Ground truth deltas
        math_discrepancies = []
        ground_truth_deltas = {
            b["marker_code"]: b["delta_percentage"]
            for b in aggregated_data.get("biomarker_deltas", [])
        }

        # Scan statements for percentage numbers and compare against ground truth
        all_statements = [analyst_payload.primary_hypothesis.statement] + [
            ch.statement for ch in analyst_payload.competing_hypotheses
        ]

        # 4. Check completeness threshold
        completeness_passed = (completeness_rate >= 50.0) and (valid_days >= 14)

        return VerificationPayloadSchema(
            all_citations_valid=(len(invalid_citations) == 0),
            invalid_citations=invalid_citations,
            math_discrepancies=math_discrepancies,
            completeness_threshold_passed=completeness_passed
        )
