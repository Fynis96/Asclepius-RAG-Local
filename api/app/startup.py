import requests
import time
import os
from .core.config import settings
import logging
from alembic import command
from alembic.config import Config

logger = logging.getLogger(__name__)

# Get the directory of the current file
current_dir = os.path.dirname(os.path.abspath(__file__))

def ensure_ollama_model():
    max_retries = 5
    for i in range(max_retries):
        try:
            response = requests.post(
                f"{settings.OLLAMA_HOST}/api/pull",
                json={"name": settings.OLLAMA_MODEL}
            )
            if response.status_code == 200:
                logger.info(f"Successfully pulled model {settings.OLLAMA_MODEL}")
                return
            else:
                logger.warning(f"Failed to pull model {settings.OLLAMA_MODEL}. Status code: {response.status_code}")
        except requests.RequestException as e:
            logger.error(f"Error connecting to Ollama: {str(e)}")
        
        if i < max_retries - 1:
            time.sleep(10)  # Wait for 10 seconds before retrying
    
    logger.error(f"Failed to pull model {settings.OLLAMA_MODEL} after {max_retries} attempts")
    
def alembic_migrations():
    try:
        logger.info("Starting Alembic migrations...")
        alembic_ini_path = os.path.join(current_dir, '..', 'alembic.ini')
        logger.info(f"Alembic.ini path: {alembic_ini_path}")
        alembic_cfg = Config(alembic_ini_path)
        logger.info("Alembic config created")
        # Set the sqlalchemy.url in the config
        alembic_cfg.set_main_option("sqlalchemy.url", settings.DATABASE_URL)
        
        logger.info("Starting upgrade to 'head'...")
        command.upgrade(alembic_cfg, "head")
        logger.info("Upgrade to 'head' completed")
        logger.info("Alembic migrations completed successfully.")
    except Exception as e:
        logger.error(f"Error during Alembic migrations: {str(e)}")
        logger.exception("Full traceback:")
        raise
        

def run_startup_tasks():
    # ensure_ollama_model()
    alembic_migrations()
    # Add other startup tasks here if needed
    
