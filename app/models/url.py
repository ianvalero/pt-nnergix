from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class UrlDB(SQLModel, table=True):
    __tablename__ = "urls"

    id: int = Field(default=None, primary_key=True)
    url: str = Field(index=True, unique=True)
    normalized_url: str | None = Field(index=True, nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))