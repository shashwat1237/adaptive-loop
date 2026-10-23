from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.enums import BiologicalSexEnum
from app.schemas.protocol import ProtocolResponse
from app.schemas.observation import BiomarkerObservationResponse
from app.schemas.confounder import ConfounderEventResponse


class MemberSummaryResponse(BaseModel):
    id: str = Field(..., example="MEM-1001")
    full_name: str
    age: int
    biological_sex: BiologicalSexEnum
    cohort: Optional[str] = "General Cohort"
    primary_goal: str
    baseline_notes: Optional[str] = None
    active_protocols_count: int
    has_completed_analysis: bool

    class Config:
        from_attributes = True


class MemberProfileSchema(BaseModel):
    id: str = Field(..., example="MEM-1001")
    full_name: str
    age: int
    biological_sex: BiologicalSexEnum
    cohort: Optional[str] = "General Cohort"
    primary_goal: str
    baseline_notes: Optional[str] = None

    class Config:
        from_attributes = True


class MemberDetailResponse(BaseModel):
    member: MemberProfileSchema
    protocols: List[ProtocolResponse]
    biomarkers: List[BiomarkerObservationResponse]
    confounders: List[ConfounderEventResponse]
