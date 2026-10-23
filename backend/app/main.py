from datetime import datetime
from fastapi import FastAPI, Request, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from app.config import settings
from app.database import engine, Base
from app.api.router import api_router

# Ensure tables are initialized on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Adaptive Loop API",
    description="Intervention Intelligence Engine — Clinical Decision Support Prototype",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Router under /api/v1
app.include_router(api_router)


# Standardized Error Envelope Handlers
@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request: Request, exc: HTTPException):
    if isinstance(exc.detail, dict) and "code" in exc.detail:
        payload = {
            "error": {
                "code": exc.detail.get("code", "HTTP_ERROR"),
                "message": exc.detail.get("message", str(exc.detail)),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "details": exc.detail.get("details", {})
            }
        }
    else:
        payload = {
            "error": {
                "code": "HTTP_ERROR",
                "message": str(exc.detail),
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "details": {"status_code": exc.status_code}
            }
        }
    return JSONResponse(status_code=exc.status_code, content=payload)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    payload = {
        "error": {
            "code": "SCHEMA_VALIDATION_ERROR",
            "message": "The request payload failed structural validation.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "details": {"errors": exc.errors()}
        }
    }
    return JSONResponse(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content=payload)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    payload = {
        "error": {
            "code": "INTERNAL_ENGINE_ERROR",
            "message": "An unhandled engine exception occurred.",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "details": {"error_type": type(exc).__name__, "description": str(exc)}
        }
    }
    return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=payload)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.PORT, reload=True)
