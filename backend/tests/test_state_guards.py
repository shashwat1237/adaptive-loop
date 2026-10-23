import pytest
from app.models.member import Member
from app.engine.coordinator import AdaptiveLoopCoordinator
from app.schemas.enums import AnalysisStatusEnum, ActionRecommendationEnum


def test_guard_insufficient_wearable_telemetry(db_session):
    # TEST-GUARD-01: Create synthetic member with only 5 days of data (C_rate < 50%)
    low_data_member = Member(
        id="MEM-TEST-LOW",
        full_name="Low Data Test",
        age=30,
        biological_sex="OTHER",
        primary_goal="Testing abstention"
    )
    db_session.add(low_data_member)
    db_session.commit()

    # Run analysis
    result = AdaptiveLoopCoordinator.run_analysis(
        member_id="MEM-TEST-LOW",
        db=db_session,
        force_recompute=True
    )

    assert result.status == AnalysisStatusEnum.ABSTAINED
    assert result.final_action == ActionRecommendationEnum.ABSTAIN_MORE_DATA_REQUIRED
    assert result.analyst_payload is None
    assert result.critic_payload is None
    assert result.verification_payload.completeness_threshold_passed is False


def test_guard_severe_nonadherence(db_session):
    # TEST-GUARD-02: David Chen (MEM-1003) has 27.8% adherence (< 40.0%)
    result = AdaptiveLoopCoordinator.run_analysis(
        member_id="MEM-1003",
        db=db_session,
        force_recompute=True
    )

    assert result.protocol_adherence_rate < 40.0
    assert result.final_action == ActionRecommendationEnum.ABSTAIN_MORE_DATA_REQUIRED
