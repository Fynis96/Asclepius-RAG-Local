import requests
import time
from .core.config import settings
import logging

logger = logging.getLogger(__name__)

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

def run_startup_tasks():
    ensure_ollama_model()
    # Add other startup tasks here if needed