from datetime import datetime
from pydantic import BaseModel

class UrlRead(BaseModel):
    id: int
    url: str
    normalized_url: str
    created_at: datetime

class UrlCreate(BaseModel):
    url: str
    normalized_url: str