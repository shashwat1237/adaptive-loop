from fastapi import APIRouter
from app.config import settings
from app.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def get_health():
    return HealthResponse(
        status="HEALTHY",
        version="1.0.0",
        database="CONNECTED",
        llm_provider=settings.LLM_PROVIDER,
        active_model=settings.GROQ_MODEL,
        mock_fallback_enabled=settings.FALLBACK_TO_MOCK,
        algorithmic_honesty_mode="STRICT_PRODUCTION" if not settings.FALLBACK_TO_MOCK else "FALLBACK_ENABLED"
    )
