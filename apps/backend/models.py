from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=True)
    ord = Column(Integer, index=True, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
