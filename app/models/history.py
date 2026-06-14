from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.url import UrlDB
    from app.models.scraper_run import ScraperRunDB


class HistoryDB(SQLModel, table=True):
    __tablename__ = "history"

    id: int = Field(default=None, primary_key=True)
    url_id: int = Field(foreign_key="urls.id", index=True)
    scraper_run_id: int = Field(foreign_key="scraper_runs.id", index=True)

    url: "UrlDB" = Relationship()
    scraper_run: "ScraperRunDB" = Relationship()