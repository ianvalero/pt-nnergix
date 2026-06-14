import logging
from sqlmodel import Session

from app.schemas.link import LinkCreate
from app.schemas.scraper_run import ScraperRunCreate
from app.models.scraper_run import ScraperRunDB
from app.mappers.link_mapper import to_link_model


logger = logging.getLogger(f"app.{__name__}")

class ScraperRunRepository:
    def create_scraper_run(
            self,
            session: Session,
            scraper_run: ScraperRunCreate,
            links: list[LinkCreate]
    ) -> ScraperRunDB:
        db_scraper_run = ScraperRunDB(**scraper_run.model_dump())

        session.add(db_scraper_run)
        session.flush()

        db_links = []
        for link_schema in links:
            db_links.append(to_link_model(link=link_schema, scraper_run_id=db_scraper_run.id))

        db_scraper_run.links = db_links

        session.add(db_scraper_run)
        session.flush()
        session.refresh(db_scraper_run)

        return db_scraper_run