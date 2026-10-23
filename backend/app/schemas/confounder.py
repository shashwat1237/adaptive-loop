from datetime import date
from pydantic import BaseModel, Field
from app.schemas.enums import ConfounderEventTypeEnum, ConfounderSeverityEnum


class ConfounderEventResponse(BaseModel):
    id: str = Field(..., example="CONF-CAREER-W08")
    event_type: ConfounderEventTypeEnum
    description: str
    start_date: date
    end_date: date
    severity: ConfounderSeverityEnum

    class Config:
        from_attributes = True
