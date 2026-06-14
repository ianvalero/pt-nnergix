from pydantic import BaseModel


class LinkRead(BaseModel):
    id: int
    url: str
    normalized_url: str
    text: str

class LinkCreate(BaseModel):
    url: str
    normalized_url: str
    text: str
