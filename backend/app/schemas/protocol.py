from datetime import date
from pydantic import BaseModel, Field
from app.schemas.enums import ProtocolCategoryEnum


class ProtocolResponse(BaseModel):
    id: str = Field(..., example="PROT-CARDIO-01")
    name: str
    category: ProtocolCategoryEnum
    dosage_or_frequency: str
    start_date: date
    review_date: date
    target_adherence_rate: float

    class Config:
        from_attributes = True
