# app/src/main.py
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, Request
from routes.users import router as users_router
from utils.logger import get_logger
from prometheus_fastapi_instrumentator import Instrumentator

# Initialize logger
logger = get_logger(__name__)

app = FastAPI(title="User Management API", description="API for user management with structured logging", version="1.0.0")

# Instrument the app with Prometheus metrics FIRST
Instrumentator().instrument(app).expose(app)

# Include routers
app.include_router(users_router, prefix="/api/v1", tags=["users"])

@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware to log all incoming requests and their responses.
    This generates valuable metrics for monitoring.
    """
    logger.info("Incoming request", extra={
        "path": request.url.path,
        "method": request.method,
        "query_params": dict(request.query_params),
    })
    
    try:
        response = await call_next(request)
        logger.info("Request completed", extra={
            "path": request.url.path,
            "method": request.method,
            "status_code": response.status_code
        })
        return response
    except Exception as e:
        logger.error("Request failed", extra={
            "path": request.url.path,
            "method": request.method,
            "error": str(e)
        })
        raise

@app.get("/")
async def root():
    logger.info("Root endpoint accessed")
    return {"message": "User Management API is running"}

@app.get("/health")
async def health_check():
    logger.info("Health check endpoint accessed")
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)