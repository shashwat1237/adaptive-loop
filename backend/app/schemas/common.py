from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class HealthResponse(BaseModel):
    status: str
    version: str
    database: str
    llm_provider: str
    active_model: str
    mock_fallback_enabled: bool = False
    algorithmic_honesty_mode: str = "STRICT_PRODUCTION"


class ErrorDetailSchema(BaseModel):
    code: str
    message: str
    timestamp: datetime
    details: Optional[Dict[str, Any]] = None


class ErrorEnvelopeResponse(BaseModel):
    error: ErrorDetailSchema
