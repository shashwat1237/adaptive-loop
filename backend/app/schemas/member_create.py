from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.enums import BiologicalSexEnum


class ProtocolCreateInput(BaseModel):
    name: str = Field(..., example="Citrus Bergamot 500mg")
    category: str = Field("SUPPLEMENT", example="SUPPLEMENT")  # LIFESTYLE, SUPPLEMENT, EXERCISE, NUTRITION
    dosage_or_frequency: str = Field(..., example="500 mg daily with evening meal")
    target_adherence_rate: float = Field(80.0, ge=0.0, le=100.0)


class BiomarkerCreateInput(BaseModel):
    marker_code: str = Field(..., example="APOB")
    marker_name: str = Field(..., example="Apolipoprotein B")
    baseline_value: float = Field(..., example=128.0)
    followup_value: float = Field(..., example=102.0)
    unit: str = Field(..., example="mg/dL")
    optimal_range_min: float = Field(..., example=40.0)
    optimal_range_max: float = Field(..., example=80.0)


class ConfounderCreateInput(BaseModel):
    event_type: str = Field("ILLNESS", example="ILLNESS")  # ILLNESS, TRAVEL, LIFE_STRESS, INJURY
    description: str = Field(..., example="Acute upper respiratory viral infection")
    start_week: int = Field(8, ge=1, le=26)
    duration_days: int = Field(14, ge=1, le=60)
    severity: str = Field("MODERATE", example="MODERATE")  # MILD, MODERATE, SEVERE


class MemberCreateRequest(BaseModel):
    id: Optional[str] = Field(None, example="MEM-2001")
    full_name: str = Field(..., min_length=2, max_length=128, example="Dr. Samantha Reed")
    age: int = Field(..., ge=18, le=120, example=45)
    biological_sex: BiologicalSexEnum = Field(BiologicalSexEnum.FEMALE)
    cohort: str = Field("Cardiometabolic Risk", max_length=64, example="Cardiometabolic Risk")
    primary_goal: str = Field(..., min_length=3, max_length=256, example="ApoB reduction & autonomic nervous system resilience")
    baseline_notes: Optional[str] = Field(None, example="Patient with elevated baseline ApoB and work-related evening sleep disturbance.")

    # Telemetry profile configuration
    telemetry_profile: str = Field("clean_responder", example="clean_responder")  # clean_responder, confounded_responder, non_adherent, custom
    baseline_resting_hr: float = Field(68.0, ge=40.0, le=120.0)
    baseline_hrv_rmssd: float = Field(36.0, ge=10.0, le=150.0)
    baseline_deep_sleep_hours: float = Field(1.1, ge=0.0, le=5.0)
    baseline_total_sleep_hours: float = Field(6.8, ge=2.0, le=14.0)

    followup_resting_hr: Optional[float] = Field(62.0)
    followup_hrv_rmssd: Optional[float] = Field(48.0)
    followup_deep_sleep_hours: Optional[float] = Field(1.6)
    followup_total_sleep_hours: Optional[float] = Field(7.3)

    protocols: Optional[List[ProtocolCreateInput]] = None
    biomarkers: Optional[List[BiomarkerCreateInput]] = None
    confounders: Optional[List[ConfounderCreateInput]] = None
