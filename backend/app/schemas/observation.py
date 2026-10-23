from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from app.schemas.confounder import ConfounderEventResponse


class BiomarkerObservationResponse(BaseModel):
    id: str = Field(..., example="OBS-BIO-APOB-D0")
    marker_code: str
    marker_name: str
    value: float
    unit: str
    optimal_range_min: float
    optimal_range_max: float
    measurement_date: date
    test_cycle_day: int = Field(..., description="0 for baseline, 180 for follow-up")

    class Config:
        from_attributes = True


class WearableDailyRecordResponse(BaseModel):
    recorded_date: date
    week_number: int
    total_sleep_hours: Optional[float] = None
    deep_sleep_hours: Optional[float] = None
    rem_sleep_hours: Optional[float] = None
    resting_heart_rate: Optional[float] = None
    hrv_rmssd: Optional[float] = None
    strain_score: Optional[float] = None
    adherence_logged: bool = False

    class Config:
        from_attributes = True


class WeeklyRollupResponse(BaseModel):
    week_number: int
    avg_total_sleep_hours: Optional[float] = None
    avg_deep_sleep_hours: Optional[float] = None
    avg_resting_heart_rate: Optional[float] = None
    avg_hrv_rmssd: Optional[float] = None
    avg_strain_score: Optional[float] = None
    adherence_rate: float
    observation_ids: List[str]


class TimelineResponse(BaseModel):
    member_id: str
    total_days_expected: int = 180
    total_days_recorded: int
    data_completeness_rate: float
    protocol_adherence_rate: float
    daily_records: List[WearableDailyRecordResponse]
    weekly_rollups: List[WeeklyRollupResponse]
    confounders: List[ConfounderEventResponse]
