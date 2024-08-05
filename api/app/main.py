import time
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from .core.database import engine, Base
from .models import user, knowledgebase, document
from .api.endpoints import auth, knowledgebase, user
from .core.minio_client import ensure_bucket_exists
from .core.config import settings
from .core.logger import logger
from .startup import run_startup_tasks


def wait_for_db(max_retries=5, retry_interval=5, timeout=10):
    retries = 0
    while retries < max_retries:
        try:
            # Attempt to create a connection with a timeout
            with engine.connect().execution_options(timeout=timeout) as connection:
                logger.info("Successfully connected to the database")
                break
        except OperationalError as e:
            retries += 1
            logger.warning(f"Database connection attempt {retries}/{max_retries} failed. Error: {str(e)}")
            logger.info(f"Retrying in {retry_interval} seconds...")
            time.sleep(retry_interval)
    else:
        logger.error("Unable to connect to the database after multiple retries")
        raise Exception("Unable to connect to the database after multiple retries")

logger.info("Waiting for database connection...")
wait_for_db()

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    logger.info("Running startup event...")
    try:
        # Create tables
        logger.info("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully.")

        # Ensure MinIO bucket exists
        logger.info("Ensuring MinIO bucket exists...")
        ensure_bucket_exists(settings.MINIO_BUCKET_NAME)
        logger.info("MinIO bucket check completed.")
        
        logger.info("Running startup tasks...")
        run_startup_tasks()
        
        logger.info("Startup tasks completed successfully.")
    except Exception as e:
        logger.error(f"Error during startup: {str(e)}")
        logger.exception("Full traceback:")
        raise
    
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
