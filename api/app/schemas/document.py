from pydantic import BaseModel

class DocumentBase(BaseModel):
    filename: str
    file_type: str

class DocumentCreate(DocumentBase):
    pass

class Document(DocumentBase):
    id: int
    file_path: str
    knowledgebase_id: int

    class Config:
        from_attributes = True