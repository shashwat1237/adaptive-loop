import uuid
import logging
from datetime import datetime
from typing import Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models.member import Member
from app.models.analysis import AnalysisRun
from app.schemas.enums import AnalysisStatusEnum, ActionRecommendationEnum
from app.schemas.analysis import AnalysisRunResponse
from app.engine.aggregator import DataAggregator
from app.engine.analyst import AIAnalyst
from app.engine.citation_checker import CitationChecker
from app.engine.critic import AICritic

logger = logging.getLogger(__name__)


class AdaptiveLoopCoordinator:
    @staticmethod
    def run_analysis(
        member_id: str,
        db: Session,
        force_recompute: bool = False
    ) -> AnalysisRunResponse:
        """Executes the full 4-stage Adaptive Loop analysis pipeline:
        Stage 1: Pandas Data Aggregator
        Guard: Principled Abstention Guard
        Stage 2: AI Analyst (LLM)
        Stage 3: Deterministic Evidence Checker (Python)
        Stage 4: AI Critic (LLM Adversarial Audit)
        Reconciliation & Persistence
        """
        # 1. Fetch Member & Longitudinal Data
        member = db.query(Member).filter(Member.id == member_id).first()
        if not member:
            raise ValueError(f"Member with ID '{member_id}' not found.")

        # Check existing latest completed analysis if not force_recompute
        if not force_recompute:
            existing = (
                db.query(AnalysisRun)
                .filter(AnalysisRun.member_id == member_id)
                .order_by(AnalysisRun.triggered_at.desc())
                .first()
            )
            if existing and existing.status in [AnalysisStatusEnum.COMPLETED.value, AnalysisStatusEnum.ABSTAINED.value]:
                return AnalysisRunResponse.model_validate(existing)

        run_id = f"ANL-{uuid.uuid4()}"
        triggered_at = datetime.utcnow()

        # 2. Stage 1: Mathematical Aggregation
        aggregated_data = DataAggregator.process_longitudinal_data(
            biomarkers=member.biomarkers,
            wearables=member.wearables,
            confounders=member.confounders
        )

        completeness_rate = aggregated_data["data_completeness_rate"]
        adherence_rate = aggregated_data["protocol_adherence_rate"]
        valid_days = aggregated_data["valid_days"]

        input_summary = {
            "biomarker_deltas": aggregated_data["biomarker_deltas"],
            "wearable_trend_summary": (
                f"Data completeness: {completeness_rate}% across {valid_days} valid recorded days."
            ),
            "adherence_summary": f"{adherence_rate}% adherence logged across active protocol period.",
            "confounders_present": [c["id"] for c in aggregated_data["confounders"]]
        }

        # 3. Principled Abstention Guard Check
        if completeness_rate < 50.0 or adherence_rate < 40.0 or valid_days < 14:
            logger.info(f"Principled Abstention triggered for member {member_id}: Completeness {completeness_rate}%, Adherence {adherence_rate}%")
            verification_payload = {
                "all_citations_valid": True,
                "invalid_citations": [],
                "math_discrepancies": [],
                "completeness_threshold_passed": False
            }

            analysis_run = AnalysisRun(
                id=run_id,
                member_id=member_id,
                triggered_at=triggered_at,
                status=AnalysisStatusEnum.ABSTAINED.value,
                final_action=ActionRecommendationEnum.ABSTAIN_MORE_DATA_REQUIRED.value,
                critic_verdict=None,
                data_completeness_rate=completeness_rate,
                protocol_adherence_rate=adherence_rate,
                input_summary_snapshot=input_summary,
                analyst_payload=None,
                verification_payload=verification_payload,
                critic_payload=None
            )
            db.add(analysis_run)
            db.commit()
            db.refresh(analysis_run)
            return AnalysisRunResponse.model_validate(analysis_run)

        # 4. Stage 2: AI Analyst
        analyst_payload = AIAnalyst.generate_analysis(
            member=member,
            protocols=member.protocols,
            aggregated_data=aggregated_data
        )

        # 5. Stage 3: Deterministic Evidence Checker
        verification_result = CitationChecker.verify(
            analyst_payload=analyst_payload,
            aggregated_data=aggregated_data
        )

        # 6. Stage 4: AI Critic
        critic_payload = AICritic.audit_analysis(
            member_id=member_id,
            analyst_payload=analyst_payload,
            aggregated_data=aggregated_data,
            verification_result=verification_result
        )

        # 7. Final Action Reconciliation
        if critic_payload.overruled_action is not None:
            final_action = critic_payload.overruled_action.value
        else:
            final_action = analyst_payload.initial_action_recommendation.value

        # Enforce severe non-adherence override if adherence < 40%
        if adherence_rate < 40.0:
            final_action = ActionRecommendationEnum.ABSTAIN_MORE_DATA_REQUIRED.value

        analysis_run = AnalysisRun(
            id=run_id,
            member_id=member_id,
            triggered_at=triggered_at,
            status=AnalysisStatusEnum.COMPLETED.value,
            final_action=final_action,
            critic_verdict=critic_payload.verdict.value,
            data_completeness_rate=completeness_rate,
            protocol_adherence_rate=adherence_rate,
            input_summary_snapshot=input_summary,
            analyst_payload=analyst_payload.model_dump(),
            verification_payload=verification_result.model_dump(),
            critic_payload=critic_payload.model_dump()
        )

        db.add(analysis_run)
        db.commit()
        db.refresh(analysis_run)

        return AnalysisRunResponse.model_validate(analysis_run)
