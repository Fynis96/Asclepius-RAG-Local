from pydantic import BaseModel

class KnowledgebaseBase(BaseModel):
    name: str
    description: str | None = None

class KnowledgebaseCreate(KnowledgebaseBase):
    pass

class KnowledgebaseUpdate(BaseModel):
    name: str | None = None
    description: str | None = None

class Knowledgebase(KnowledgebaseBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True
