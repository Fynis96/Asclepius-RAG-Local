from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from ...core.database import get_db
from ...crud import knowledgebase as crud_knowledgebase, document as crud_document
from ...schemas.knowledgebase import Knowledgebase, KnowledgebaseCreate, KnowledgebaseUpdate
from ...schemas.document import Document, DocumentCreate
from ...schemas.user import User
from ..deps import get_current_user

router = APIRouter()

@router.post("/knowledgebases/", response_model=Knowledgebase)
def create_knowledgebase(
    knowledgebase: KnowledgebaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_knowledgebase.create_knowledgebase(db=db, knowledgebase=knowledgebase, user_id=current_user.id)

@router.get("/knowledgebases/", response_model=List[Knowledgebase])
def read_knowledgebases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return crud_knowledgebase.get_knowledgebases(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/knowledgebases/{knowledgebase_id}", response_model=Knowledgebase)
def read_knowledgebase(
    knowledgebase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not knowledgebase or knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    return knowledgebase

@router.put("/knowledgebases/{knowledgebase_id}", response_model=Knowledgebase)
def update_knowledgebase(
    knowledgebase_id: int,
    knowledgebase: KnowledgebaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not db_knowledgebase or db_knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    return crud_knowledgebase.update_knowledgebase(db, db_knowledgebase, knowledgebase)

@router.delete("/knowledgebases/{knowledgebase_id}", response_model=Knowledgebase)
def delete_knowledgebase(
    knowledgebase_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not db_knowledgebase or db_knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    return crud_knowledgebase.delete_knowledgebase(db, db_knowledgebase)

@router.post("/knowledgebases/{knowledgebase_id}/documents/", response_model=Document)
async def create_document(
    knowledgebase_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not knowledgebase or knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    
    document = DocumentCreate(filename=file.filename, file_type=file.content_type)
    return crud_document.create_document(db=db, document=document, knowledgebase_id=knowledgebase_id, file_content=await file.read())

@router.get("/knowledgebases/{knowledgebase_id}/documents/", response_model=List[Document])
def read_documents(
    knowledgebase_id: int,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not knowledgebase or knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    
    return crud_document.get_documents(db, knowledgebase_id=knowledgebase_id, skip=skip, limit=limit)

@router.delete("/knowledgebases/{knowledgebase_id}/documents/{document_id}", response_model=Document)
def delete_document(
    knowledgebase_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    knowledgebase = crud_knowledgebase.get_knowledgebase(db, knowledgebase_id)
    if not knowledgebase or knowledgebase.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Knowledgebase not found")
    
    document = crud_document.get_document(db, document_id)
    if not document or document.knowledgebase_id != knowledgebase_id:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return crud_document.delete_document(db, document)