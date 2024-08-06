from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.api.deps import get_current_user, get_db
from app.crud import index as crud_index
from app.schemas.index import IndexCreate, IndexResponse, IndexUpdate
from app.models.user import User
from app.services.index_service import IndexService
from app.crud import knowledgebase as crud_knowledgebase

router = APIRouter()

@router.post("/run/{knowledgebase_id}")
async def run_knowledgebase_indexing(
    knowledgebase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not knowledgebase or knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    
    index_service = IndexService()
    await index_service.create_index(knowledgebase_id)
    return {"message": "Indexing process started successfully"}

@router.post("/", response_model=IndexResponse)
async def create_index(
    index: IndexCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_index = crud_index.create_index(db, index)
    return db_index

@router.get("/{index_id}", response_model=IndexResponse)
def get_index(
    index_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_index = crud_index.get_index(db, index_id)
    if db_index is None:
        raise HTTPException(status_code=404, detail="Index not found")
    return db_index

@router.delete("/{index_id}", response_model=IndexResponse)
async def delete_index(
    index_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_index = crud_index.get_index(db, index_id)
    if db_index is None:
        raise HTTPException(status_code=404, detail="Index not found")
    
    index_service = IndexService()
    await index_service.delete_index(index_id)
    
    return crud_index.delete_index(db, index_id)

@router.put("/{index_id}", response_model=IndexResponse)
def update_index(
    index_id: int,
    index_update: IndexUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_index = crud_index.get_index(db, index_id)
    if db_index is None:
        raise HTTPException(status_code=404, detail="Index not found")
    
    updated_index = crud_index.update_index(db, db_index, index_update)
    return updated_index
