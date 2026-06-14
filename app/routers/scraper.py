import logging
from fastapi import APIRouter, status, Depends
from sqlmodel import Session

from app.mappers.history_mapper import to_history_schema
from app.schemas.history import History
from app.schemas.scraper_run import ScraperRunPayload
from app.database import get_session
import app.dependencies as dependencies
from app.services.history_service import HistoryService

logger = logging.getLogger(f"app.{__name__}")

router = APIRouter(prefix="/scraper", tags=["scraper"])

@router.post(
    "/",
    response_model=History,
    status_code=status.HTTP_201_CREATED,
    summary="Extract links from URL"
)
async def extract_links(
    payload: ScraperRunPayload,
    session: Session = Depends(get_session),
    history_repository = Depends(dependencies.get_history_repository),
    history_service: HistoryService = Depends(dependencies.get_history_service)
):
    db_history = await history_service.create(session=session, payload=payload)
    return to_history_schema(history_repository.get_history_by_id(session=session, history_id=db_history.id))