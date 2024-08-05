from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from ..core.database import Base
from .timestamp import TimestampMixin

class Knowledgebase(Base, TimestampMixin):
    __tablename__ = "knowledgebases"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    index_id = Column(Integer, ForeignKey("indexes.id"))
    is_indexed = Column(Boolean, default=False)
    
    index = relationship("Index", back_populates="knowledgebase")
    user = relationship("User", back_populates="knowledgebases")
    documents = relationship("Document", back_populates="knowledgebase")