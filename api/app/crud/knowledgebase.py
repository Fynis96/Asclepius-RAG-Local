from sqlalchemy.orm import Session
from ..models.knowledgebase import Knowledgebase
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

def update_knowledgebase(db: Session, db_knowledgebase: Knowledgebase, knowledgebase: KnowledgebaseUpdate):
    for key, value in knowledgebase.dict(exclude_unset=True).items():
        setattr(db_knowledgebase, key, value)
    db.commit()
    db.refresh(db_knowledgebase)
    return db_knowledgebase

def delete_knowledgebase(db: Session, db_knowledgebase: Knowledgebase):
    db.delete(db_knowledgebase)
    db.commit()
    return db_knowledgebase