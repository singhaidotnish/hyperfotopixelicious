from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    filename: str
    title: str = ""
    ord: int = 0  # display order
    created_at: datetime = Field(default_factory=datetime.utcnow)