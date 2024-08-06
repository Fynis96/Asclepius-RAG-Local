from sqlalchemy.orm import Session
from ..models.knowledgebase import Knowledgebase
from ..models.index import Index
from typing import Union
from ..schemas.knowledgebase import KnowledgebaseCreate, KnowledgebaseUpdate

def create_knowledgebase(db: Session, knowledgebase: KnowledgebaseCreate, user_id: int):
    db_knowledgebase = Knowledgebase(**knowledgebase.dict(), user_id=user_id)
    db.add(db_knowledgebase)
    db.commit()
    db.refresh(db_knowledgebase)
    return db_knowledgebase

def get_knowledgebase(db: Session, knowledgebase_id: int):
    return db.query(Knowledgebase).filter(Knowledgebase.id == knowledgebase_id).first()

def get_knowledgebases(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(Knowledgebase).filter(Knowledgebase.user_id == user_id).offset(skip).limit(limit).all()

def update_knowledgebase(db: Session, db_knowledgebase: Knowledgebase, knowledgebase: Union[KnowledgebaseUpdate, dict]):
    if isinstance(knowledgebase, dict):
        update_data = knowledgebase
    else:
        update_data = knowledgebase.dict(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(db_knowledgebase, key, value)
    db.commit()
    db.refresh(db_knowledgebase)
    return db_knowledgebase

def delete_knowledgebase(db: Session, db_knowledgebase: Knowledgebase):
    # Delete associated indexes first
    db.query(Index).filter(Index.knowledgebase_id == db_knowledgebase.id).delete()
    
    # Then delete the knowledgebase
    db.delete(db_knowledgebase)
    db.commit()
    return db_knowledgebase
