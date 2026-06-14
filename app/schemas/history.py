from datetime import datetime
from pydantic import BaseModel

from app.schemas.scraper_run import ScraperRunRead
from app.schemas.url import UrlRead


class History(BaseModel):
    id: int
    created_at: datetime
    url: UrlRead
    scraper_run: ScraperRunRead

class HistoryCreate(BaseModel):
    url_id: int
    scraper_run_id: int