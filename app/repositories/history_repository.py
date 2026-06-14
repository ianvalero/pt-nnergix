from typing import cast
from sqlmodel import Session, select, func
from sqlalchemy.orm import selectinload

from app.models.scraper_run import ScraperRunDB
from app.models.history import HistoryDB
from app.schemas.history import HistoryCreate


class HistoryRepository:
    def get_history_paginated(self, session: Session, offset: int = 0, limit: int = 100) -> tuple[list[HistoryDB], int]:
        total = cast(int, session.exec(select(func.count()).select_from(HistoryDB)).one())

        statement = (
            select(HistoryDB)
            .options(
                selectinload(HistoryDB.url),
                selectinload(HistoryDB.scraper_run).selectinload(ScraperRunDB.links)
            )
            .order_by(HistoryDB.id)
            .offset(offset)
            .limit(limit)
        )

        return cast(list[HistoryDB], session.exec(statement).all()), total

    def get_history_by_id(self, session: Session, history_id: int) -> HistoryDB | None:
        statement = (
            select(HistoryDB)
            .where(HistoryDB.id == history_id)
            .options(
                selectinload(HistoryDB.url),
                selectinload(HistoryDB.scraper_run).selectinload(ScraperRunDB.links)
            )
        )
        return session.exec(statement).one_or_none()

    def get_history_by_url_id(self, session: Session, url_id: int) -> list[HistoryDB]:
        statement= (
            select(HistoryDB)
            .where(HistoryDB.url_id == url_id)
            .options(
                selectinload(HistoryDB.url),
                selectinload(HistoryDB.scraper_run).selectinload(ScraperRunDB.links)
            )
        )
        return list(session.exec(statement).all())

    def get_history_by_scraper_run_id(self, session: Session, scraper_run_id: int) -> HistoryDB | None:
        statement = (
            select(HistoryDB)
            .where(HistoryDB.scraper_run_id == scraper_run_id)
            .options(
                selectinload(HistoryDB.url),
                selectinload(HistoryDB.scraper_run).selectinload(ScraperRunDB.links)
            )
        )
        return session.exec(statement).one_or_none()

    def create_history(self, session: Session, history_create: HistoryCreate) -> HistoryDB :
        history_db = HistoryDB(**history_create.model_dump())
        session.add(history_db)
        session.flush()
        session.refresh(history_db)

        return history_db

