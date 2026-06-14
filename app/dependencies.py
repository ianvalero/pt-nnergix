from fastapi import Request

from app.repositories.history_repository import HistoryRepository
from app.repositories.url_repository import UrlRepository
from app.repositories.scraper_run_repository import ScraperRunRepository
from app.services.scraper_service import ScraperService
from app.services.history_service import HistoryService


def get_history_repository(request: Request) -> HistoryRepository:
    return request.app.state.history_repository

def get_url_repository(request: Request) -> UrlRepository:
    return request.app.state.url_repository

def get_scraper_run_repository(request: Request) -> ScraperRunRepository:
    return request.app.state.scraper_run_repository

def get_scraper_service(request: Request) -> ScraperService:
    return request.app.state.scraper_service

def get_history_service(request: Request) -> HistoryService:
    return request.app.state.history_service