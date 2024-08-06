from sqlalchemy.orm import Session
from ..models.index import Index
from ..schemas.index import IndexCreate, IndexUpdate
from ..core.minio_client import get_minio_client
from ..core.config import settings
from typing import Union
from ..schemas.index import IndexUpdate
import uuid
import io

def create_index(
    db: Session,
    index: Union[IndexCreate, dict]
):
    if isinstance(index, dict):
        index_data = index
    else:
        index_data = index.dict()
    
    db_index = Index(**index_data)
    db.add(db_index)
    db.commit()
    db.refresh(db_index)
    
    return db_index

def get_index(db: Session, index_id: int):
    return db.query(Index).filter(Index.id == index_id).first()

def get_index_by_knowledgebase(db: Session, knowledgebase_id: int):
    return db.query(Index).filter(Index.knowledgebase_id == knowledgebase_id).first()

def get_indices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Index).offset(skip).limit(limit).all()

def delete_index(db: Session, index_id: int):
    db_index = db.query(Index).filter(Index.id == index_id).first()
    db.delete(db_index)
    db.commit()
    return db_index

def update_index(db: Session, db_index: Index, index_update: Union[IndexUpdate, dict]):
    if isinstance(index_update, IndexUpdate):
        update_data = index_update.dict(exclude_unset=True)
    else:
        update_data = index_update
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
