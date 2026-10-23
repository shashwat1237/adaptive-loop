import pytest
from app.engine.coordinator import AdaptiveLoopCoordinator
from app.schemas.enums import ActionRecommendationEnum, CriticVerdictEnum


def test_persona_clean_marcus_vance(db_session):
    # TEST-PERS-01: Marcus Vance (MEM-1001) - Clean responder
    result = AdaptiveLoopCoordinator.run_analysis(
        member_id="MEM-1001",
        db=db_session,
        force_recompute=True
    )

    assert result.member_id == "MEM-1001"
    assert result.final_action == ActionRecommendationEnum.CONTINUE_PROTOCOL
    assert result.critic_verdict == CriticVerdictEnum.APPROVED
    assert result.protocol_adherence_rate >= 80.0
    assert result.data_completeness_rate >= 90.0


def test_persona_confounded_elena_rostova(db_session):
    # TEST-PERS-02: Elena Rostova (MEM-1002) - Confounded responder
    result = AdaptiveLoopCoordinator.run_analysis(
        member_id="MEM-1002",
        db=db_session,
        force_recompute=True
    )

    assert result.member_id == "MEM-1002"
    assert result.final_action == ActionRecommendationEnum.ADJUST_WITH_CLINICIAN
    assert result.critic_verdict == CriticVerdictEnum.AMENDED
    # Critic should note confounder or attribution
    critique_lower = result.critic_payload.critique.lower()
    assert "transition" in critique_lower or "career" in critique_lower or "confound" in critique_lower or "supplement" in critique_lower


def test_persona_nonadherent_david_chen(db_session):
    # TEST-PERS-03: David Chen (MEM-1003) - Non-adherent case
    result = AdaptiveLoopCoordinator.run_analysis(
        member_id="MEM-1003",
        db=db_session,
        force_recompute=True
    )

    assert result.member_id == "MEM-1003"
    assert result.final_action == ActionRecommendationEnum.ABSTAIN_MORE_DATA_REQUIRED
    assert result.protocol_adherence_rate < 40.0
