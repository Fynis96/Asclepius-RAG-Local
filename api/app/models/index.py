from ..core.database import Base
from .timestamp import TimestampMixin
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, JSON
from sqlalchemy.orm import relationship

class Index(Base, TimestampMixin):
    __tablename__ = "indexes"

    id = Column(Integer, primary_key=True, index=True)
    qdrant_collection_name = Column(String, index=True)
    embed_model = Column(String)
    enabled_hybrid = Column(Boolean, default=False)
    index_size = Column(Integer, default=0)
    knowledgebase_id = Column(Integer, ForeignKey("knowledgebases.id"))
    document_ids = Column(JSON)    

    knowledgebase = relationship("Knowledgebase", back_populates="index")
