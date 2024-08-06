from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from .core.database import Base, engine
from .models import user, knowledgebase, document
from .api.endpoints import auth, knowledgebase, user
from .core.minio_client import ensure_bucket_exists
from .core.config import settings
from .core.logger import logger
from .startup import run_startup_tasks

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Running startup event...")
    try:
        if not run_startup_tasks():
            logger.error("Startup tasks failed. Aborting application startup.")
            raise SystemExit("Startup tasks failed")
        
        # Create tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")

        # Ensure MinIO bucket exists
        logger.info("Ensuring MinIO bucket exists...")
        ensure_bucket_exists(settings.MINIO_BUCKET_NAME)
        logger.info("MinIO bucket check completed.")
        
        logger.info("Startup tasks completed successfully.")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.exception("Full traceback:")
        raise SystemExit("Application startup failed")
    
# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.debug(f"Request: {request.method} {request.url}")
    logger.debug(f"Headers: {request.headers}")
    response = await call_next(request)
    logger.debug(f"Response status: {response.status_code}")
    return response

# Include routers
logger.info("Including routers...")
app.include_router(auth.router, prefix="/api/v1", tags=["auth"])
app.include_router(user.router, prefix="/api/v1", tags=["users"])
app.include_router(knowledgebase.router, prefix="/api/v1", tags=["knowledgebase"])

@app.get("/")
def read_root():
    return {"Hello": "World"}

logger.info("Application setup completed.")
