"""
FastAPI Application Entrypoint.
Initializes middleware, routing, CORS, and startup event lifecycle.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.logging_config import logger
from backend.api.router import api_router
from backend.utils.exceptions import BaseHelpdeskException

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    description="Enterprise Voice AI IT Helpdesk Backend with GPT-5 Function Calling & ElevenLabs Playbooks.",
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def log_requests_middleware(request, call_next):
    """Middleware injecting Correlation ID and logging HTTP request timing metrics."""
    import time
    import uuid
    request_id = request.headers.get("X-Request-ID", f"req-{uuid.uuid4().hex[:8]}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time-MS"] = f"{process_time:.2f}"

    logger.info(
        f"HTTP {request.method} {request.url.path} -> {response.status_code} ({process_time:.2f}ms) [ID: {request_id}]"
    )
    return response


# Include API Router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.exception_handler(BaseHelpdeskException)
async def helpdesk_exception_handler(request, exc: BaseHelpdeskException):
    """Global exception handler returning RFC 7807 problem details with voice fallback."""
    from fastapi.responses import JSONResponse
    logger.warning(f"Domain Exception [{exc.__class__.__name__}]: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "type": f"https://helpdesk.company.com/errors/{exc.__class__.__name__.lower()}",
            "title": exc.__class__.__name__,
            "status": exc.status_code,
            "detail": exc.message,
            "voice_fallback": exc.voice_fallback,
        },
    )


@app.on_event("startup")
async def startup_event():
    logger.info(f"Starting {settings.PROJECT_NAME} v{settings.VERSION} [{settings.ENVIRONMENT}]")


@app.on_event("shutdown")
async def shutdown_event():
    logger.info(f"Shutting down {settings.PROJECT_NAME}")


@app.get("/", summary="Root Welcome Endpoint")
async def root():
    """Welcome endpoint providing metadata links."""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
        "health": f"{settings.API_V1_STR}/health",
    }
