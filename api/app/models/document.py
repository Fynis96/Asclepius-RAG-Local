from sqlalchemy import Column, Integer, String, ForeignKey, JSON, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    file_type = Column(String)
    doc_metadata = Column(JSON, nullable=True)
    minio_bucket = Column(String)
    is_indexed = Column(Boolean, default=False)

    index_id = Column(Integer, ForeignKey("indexes.id"), nullable=True)
    knowledgebase_id = Column(Integer, ForeignKey("knowledgebases.id"))

    knowledgebase = relationship("Knowledgebase", back_populates="documents")
    index = relationship("Index", back_populates="documents")
