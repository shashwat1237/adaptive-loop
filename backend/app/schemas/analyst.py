from typing import List
from pydantic import BaseModel
from app.schemas.enums import ConfidenceLevelEnum, ActionRecommendationEnum


class HypothesisSchema(BaseModel):
    statement: str
    confidence: ConfidenceLevelEnum
    cited_observations: List[str]


class AnalystPayloadSchema(BaseModel):
    primary_hypothesis: HypothesisSchema
    competing_hypotheses: List[HypothesisSchema] = []
    unresolved_uncertainties: List[str] = []
    initial_action_recommendation: ActionRecommendationEnum = ActionRecommendationEnum.CONTINUE_PROTOCOL
