from pydantic import BaseModel
from typing import List, Optional

class IndexBase(BaseModel):
    name: str
    embed_model: str
    enabled_hybrid: bool = True
    document_ids: List[int]
    knowledgebase_id: int

class IndexCreate(IndexBase):
    pass

class IndexUpdate(BaseModel):
    name: Optional[str] = None
    embed_model: Optional[str] = None
    enabled_hybrid: Optional[bool] = None
    document_ids: Optional[List[int]] = None

class IndexResponse(IndexBase):
    id: int
    qdrant_collection_name: str
    index_size: int

    class Config:
        from_attributes = True
