from app.schemas.history import History
from app.models.history import HistoryDB
from app.schemas.url import UrlRead
from app.schemas.scraper_run import ScraperRunRead

def to_history_schema(db: HistoryDB) -> History:
    return History(
        id=db.id,
        created_at=db.url.created_at,
        url=UrlRead.model_validate(db.url, from_attributes=True),
        scraper_run=ScraperRunRead.model_validate(db.scraper_run, from_attributes=True)
    )