import logging
from sqlmodel import Session

from app.repositories.history_repository import HistoryRepository
from app.repositories.scraper_run_repository import ScraperRunRepository
from app.repositories.url_repository import UrlRepository
from app.services.scraper_service import ScraperService
from app.schemas.url import UrlCreate
from app.schemas.scraper_run import ScraperRunPayload, ScraperRunCreate
from app.schemas.history import HistoryCreate
from app.models.history import HistoryDB


class HistoryService:

    def __init__(
        self,
        scraper_service: ScraperService,
        url_repository: UrlRepository,
        scraper_run_repository: ScraperRunRepository,
        history_repository: HistoryRepository
    ):
        self.logger = logging.getLogger(f"app.{__name__}")
        self.scraper_service = scraper_service
        self.url_repository = url_repository
        self.scraper_run_repository = scraper_run_repository
        self.history_repository = history_repository

        self.logger.info("History Service initialized")

    async def create(self,session: Session, payload: ScraperRunPayload) -> HistoryDB:
        scraper_result = await self.scraper_service.scrape_url(payload)

        try:
            normalized = UrlRepository.normalize_url(payload.url)
            db_url = self.url_repository.get_or_create_url(
                session=session,
                url=UrlCreate(url=payload.url, normalized_url=normalized)
            )

            db_scraper_run = self.scraper_run_repository.create_scraper_run(
                session=session,
                scraper_run=ScraperRunCreate(
                    url_id=db_url.id,
                    status=scraper_result.status,
                    http_status=scraper_result.http_status,
                    response_time_ms=scraper_result.response_time_ms,
                    follow_redirects=scraper_result.follow_redirects,
                    error_message=scraper_result.error_message
                ),
                links=scraper_result.links
            )

            db_history = self.history_repository.create_history(
                session=session,
                history_create=HistoryCreate(url_id=db_url.id, scraper_run_id=db_scraper_run.id)
            )

            session.commit()
            session.refresh(db_history)
            return db_history

        except Exception:
            session.rollback()
            raise