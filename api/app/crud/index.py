from sqlalchemy.orm import Session
from ..models.index import Index
from ..schemas.index import IndexCreate, IndexUpdate
from ..core.minio_client import get_minio_client
from ..core.config import settings
import uuid
import io

def create_index(
    db: Session,
    index: IndexCreate
):
    qdrant_collection_name = f"collection_{index.id}_{index.knowledgebase_id}"
    db_index = Index(**index.dict(), qdrant_collection_name=qdrant_collection_name)
    db.add(db_index)
    db.commit()
    db.refresh(db_index)
    return db_index

def get_index(db: Session, index_id: int):
    return db.query(Index).filter(Index.id == index_id).first()

def get_indices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Index).offset(skip).limit(limit).all()

def delete_index(db: Session, index_id: int):
    db_index = db.query(Index).filter(Index.id == index_id).first()
    db.delete(db_index)
    db.commit()
    return db_index

def update_index(db: Session, db_index: Index, index_update: IndexUpdate):
    update_data = index_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_index, key, value)
    db.commit()
    db.refresh(db_index)
    return db_index

def update_index_size(db: Session, index_id: int, new_size: int):
    db_index = get_index(db, index_id)
    if db_index:
        db_index.index_size = new_size
        db.commit()
        db.refresh(db_index)
    return db_index