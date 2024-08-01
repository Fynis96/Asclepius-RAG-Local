from sqlalchemy.orm import Session
from ..models.document import Document
from ..schemas.document import DocumentCreate
from ..core.minio_client import get_minio_client
from ..core.config import settings
import uuid
import io

def create_document(db: Session, document: DocumentCreate, knowledgebase_id: int, file_content: bytes):
    minio_client = get_minio_client()
    file_uuid = str(uuid.uuid4())
    file_path = f"{knowledgebase_id}/{file_uuid}/{document.filename}"
    
    file_data = io.BytesIO(file_content)
    
    minio_client.put_object(
        bucket_name=settings.MINIO_BUCKET_NAME,
        object_name=file_path,
        data=file_data,
        length=len(file_content),
        content_type=document.file_type
    )

    db_document = Document(
        filename=document.filename,
        file_path=file_path,
        file_type=document.file_type,
        knowledgebase_id=knowledgebase_id
    )
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

def get_document(db: Session, document_id: int):
    return db.query(Document).filter(Document.id == document_id).first()

def get_documents(db: Session, knowledgebase_id: int, skip: int = 0, limit: int = 100):
    return db.query(Document).filter(Document.knowledgebase_id == knowledgebase_id).offset(skip).limit(limit).all()

def delete_document(db: Session, db_document: Document):
    minio_client = get_minio_client()
    
    # Delete the file from MinIO
    minio_client.remove_object(settings.MINIO_BUCKET_NAME, db_document.file_path)
    
    # Delete the document record from the database
    db.delete(db_document)
    db.commit()
    return db_document