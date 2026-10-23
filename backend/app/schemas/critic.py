from typing import Any, Dict, List, Optional
from pydantic import BaseModel
from app.schemas.enums import CriticVerdictEnum, ActionRecommendationEnum


class VerificationPayloadSchema(BaseModel):
    all_citations_valid: bool
    invalid_citations: List[str]
    math_discrepancies: List[Dict[str, Any]]
    completeness_threshold_passed: bool


class CriticPayloadSchema(BaseModel):
    verdict: CriticVerdictEnum = CriticVerdictEnum.APPROVED
    critique: str = "Clinical reasoning verified and audited."
    identified_cognitive_biases: List[str] = []
    overruled_action: Optional[ActionRecommendationEnum] = None
    action_rationale: str = "Evidence alignment confirmed."
