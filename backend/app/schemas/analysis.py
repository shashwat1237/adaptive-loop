from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, Field
from app.schemas.enums import AnalysisStatusEnum, ActionRecommendationEnum, CriticVerdictEnum
from app.schemas.analyst import AnalystPayloadSchema
from app.schemas.critic import VerificationPayloadSchema, CriticPayloadSchema


class AnalysisCreateRequest(BaseModel):
    member_id: str = Field(..., example="MEM-1002")
    force_recompute: bool = False


class AnalysisRunResponse(BaseModel):
    id: str = Field(..., example="ANL-9f8e4c2b-6a1d-4e89-b2c3-4d5e6f7a8b9c")
    member_id: str
    triggered_at: datetime
    status: AnalysisStatusEnum
    final_action: ActionRecommendationEnum
    critic_verdict: Optional[CriticVerdictEnum] = None
    data_completeness_rate: float
    protocol_adherence_rate: float
    input_summary_snapshot: Dict[str, Any]
    analyst_payload: Optional[AnalystPayloadSchema] = None
    verification_payload: Optional[VerificationPayloadSchema] = None
    critic_payload: Optional[CriticPayloadSchema] = None

    class Config:
        from_attributes = True
