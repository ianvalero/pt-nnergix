import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, APIRouter
from fastapi.responses import JSONResponse

from app.config.log import setup_logging
from app.repositories.history_repository import HistoryRepository
from app.repositories.url_repository import UrlRepository
from app.repositories.scraper_run_repository import ScraperRunRepository
from app.services.scraper_service import ScraperService
from app.services.history_service import HistoryService
from app.routers import history, scraper


logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    setup_logging()
    logger = logging.getLogger(f"app.{__name__}")
    logger.info("App starting")

    app.state.history_repository = HistoryRepository()
    app.state.url_repository = UrlRepository()
    app.state.scraper_run_repository = ScraperRunRepository()
    app.state.scraper_service = ScraperService()
    app.state.history_service = HistoryService(
        scraper_service=app.state.scraper_service,
        url_repository=app.state.url_repository,
        scraper_run_repository=app.state.scraper_run_repository,
        history_repository=app.state.history_repository
    )

    yield
    logger.info("App shutting down")

app = FastAPI(
    title="Link extractor",
    description="API for extracting links from URLs",
    version="0.1.0",
    lifespan=lifespan
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.exception(
        "Unhandled error on %s %s",
        request.method,
        request.url.path,
    )

    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"},
    )

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(history.router)
api_v1_router.include_router(scraper.router)

app.include_router(api_v1_router)