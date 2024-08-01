from minio import Minio
from minio.error import S3Error
from ..core.config import settings
from ..core.logger import logger

def get_minio_client():
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_SECURE
    )

def ensure_bucket_exists(bucket_name: str):
    client = get_minio_client()
    try:
        if not client.bucket_exists(bucket_name):
            client.make_bucket(bucket_name)
            logger.info(f"Bucket '{bucket_name}' created successfully")
        else:
            logger.info(f"Bucket '{bucket_name}' already exists")
            
    except S3Error as e:
        logger.error(f"Error occurred while creating bucket: {e}")
        raise