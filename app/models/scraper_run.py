from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime, timezone
from enum import Enum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.link import LinkDB


class ScraperStatus(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

class ScraperRunDB(SQLModel, table=True):
    __tablename__ = "scraper_runs"

    id: int = Field(default=None, primary_key=True)
    url_id: int = Field(foreign_key="urls.id", index=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    status: ScraperStatus = Field(index=True)
    http_status: int = Field()
    response_time_ms: int = Field()
    follow_redirects: bool = Field()
    error_message: str | None = Field(default=None, nullable=True)

    links: list["LinkDB"] = Relationship()