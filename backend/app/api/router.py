from fastapi import APIRouter
from app.api.health import router as health_router
from app.api.members import router as members_router
from app.api.analyses import router as analyses_router

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(health_router, tags=["Health"])
api_router.include_router(members_router, tags=["Members"])
api_router.include_router(analyses_router, tags=["Analyses"])
