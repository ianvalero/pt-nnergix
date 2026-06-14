from datetime import datetime
from pydantic import BaseModel, Field, model_validator

from app.models.scraper_run import ScraperStatus
from app.schemas.link import LinkRead, LinkCreate

class ScraperRunPayload(BaseModel):
    url: str
    follow_redirects: bool = True
    timeout: int | float = Field(default=10.0, gt=0, le=30.0)

class ScraperRunBase(BaseModel):
    status: ScraperStatus
    http_status: int
    response_time_ms: int
    follow_redirects: bool = True
    error_message: str | None = None

class ScraperRunResult(ScraperRunBase):
    links: list[LinkCreate] = []

class ScraperRunCreate(ScraperRunBase):
    url_id: int

class ScraperRunRead(ScraperRunBase):
    id: int
    created_at: datetime
    links_count: int = 0
    links: list[LinkRead] = Field(default_factory=list)

    @model_validator(mode='after')
    def calculate_links_count(self) -> 'ScraperRunRead':
        self.links_count = len(self.links)
        return self