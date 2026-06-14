import logging
from sqlmodel import Session, select
from urllib.parse import urlparse, urlunparse

from app.models.url import UrlDB
from app.schemas.url import UrlCreate


logger = logging.getLogger(f"app.{__name__}")

class UrlRepository:
    def get_or_create_url(self, session: Session, url: UrlCreate) -> UrlDB:
        url_bd = session.exec(
            select(UrlDB).
            where(UrlDB.normalized_url == url.normalized_url)
        ).one_or_none()

        if url_bd is not None:
            return url_bd

        return self.__create_url(session, url)

    @staticmethod
    def normalize_url(url: str) -> str:
        parsed_url = urlparse(url.strip())

        scheme = parsed_url.scheme.lower()
        netloc = parsed_url.netloc.lower()
        path = parsed_url.path.rstrip("/") or "/"

        return urlunparse((scheme, netloc, path, "", "", ""))

    def __create_url(self, session: Session, url: UrlCreate) -> UrlDB:
         db_url: UrlDB = UrlDB(**url.model_dump())
         session.add(db_url)
         session.flush()

         logger.info(f"URL {db_url.normalized_url} created")
         return db_url
