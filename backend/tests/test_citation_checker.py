import pytest
from app.engine.citation_checker import CitationChecker
from app.schemas.analyst import AnalystPayloadSchema, HypothesisSchema
from app.schemas.enums import ConfidenceLevelEnum, ActionRecommendationEnum


def test_citation_checker_valid_citations():
    # TEST-CITE-01: Valid registered citations
    registry = {
        "OBS-BIO-APOB-D180": {"type": "BIOMARKER"},
        "OBS-WEAR-DEEP-W24": {"type": "WEARABLE_WEEKLY"}
    }
    aggregated = {
        "observation_registry": registry,
        "data_completeness_rate": 95.0,
        "valid_days": 170,
        "biomarker_deltas": []
    }
    analyst_payload = AnalystPayloadSchema(
        primary_hypothesis=HypothesisSchema(
            statement="ApoB dropped significantly.",
            confidence=ConfidenceLevelEnum.HIGH,
            cited_observations=["OBS-BIO-APOB-D180"]
        ),
        competing_hypotheses=[
            HypothesisSchema(
                statement="Deep sleep also improved.",
                confidence=ConfidenceLevelEnum.MODERATE,
                cited_observations=["OBS-WEAR-DEEP-W24"]
            )
        ],
        unresolved_uncertainties=[],
        initial_action_recommendation=ActionRecommendationEnum.CONTINUE_PROTOCOL
    )

    result = CitationChecker.verify(analyst_payload, aggregated)
    assert result.all_citations_valid is True
    assert result.invalid_citations == []
    assert result.completeness_threshold_passed is True


def test_citation_checker_hallucinated_citations():
    # TEST-CITE-02: Hallucinated observation ID
    registry = {
        "OBS-BIO-APOB-D180": {"type": "BIOMARKER"}
    }
    aggregated = {
        "observation_registry": registry,
        "data_completeness_rate": 95.0,
        "valid_days": 170,
        "biomarker_deltas": []
    }
    analyst_payload = AnalystPayloadSchema(
        primary_hypothesis=HypothesisSchema(
            statement="ApoB dropped.",
            confidence=ConfidenceLevelEnum.HIGH,
            cited_observations=["OBS-BIO-APOB-D180", "OBS-FAKE-XYZ-D99"]
        ),
        competing_hypotheses=[],
        unresolved_uncertainties=[],
        initial_action_recommendation=ActionRecommendationEnum.CONTINUE_PROTOCOL
    )

    result = CitationChecker.verify(analyst_payload, aggregated)
    assert result.all_citations_valid is False
    assert "OBS-FAKE-XYZ-D99" in result.invalid_citations
