from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from ..core.database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    file_path = Column(String)
    file_type = Column(String)
    knowledgebase_id = Column(Integer, ForeignKey("knowledgebases.id"))

    knowledgebase = relationship("Knowledgebase", back_populates="documents")