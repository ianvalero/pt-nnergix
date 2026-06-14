from fastapi import APIRouter, HTTPException, status, Depends, Query
from sqlmodel import Session

from app.schemas.history import History
from app.schemas.pagination import Pagination, PaginatedResponse
from app.mappers.history_mapper import to_history_schema
from app.database import get_session
import app.dependencies as dependencies


router = APIRouter(prefix="/history", tags=["history"])

@router.get(
    "/",
    response_model=PaginatedResponse[History],
    status_code=status.HTTP_200_OK,
    summary="Get all history"
)
async def get_history(
    offset: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session),
    history_repository = Depends(dependencies.get_history_repository)
):
    items, total = history_repository.get_history_paginated(session=session, offset=offset, limit=limit)
    pagination = Pagination(
        offset=offset,
        limit=limit,
        total=total,
        has_next=offset + limit < total,
        has_prev=offset>0
    )

    return PaginatedResponse[History](
        items=[to_history_schema(item) for item in items],
        pagination=pagination
    )


@router.get(
    "/{history_id}/",
    response_model=History,
    status_code=status.HTTP_200_OK,
    summary="Get history by id"
)
async def get_history_by_id(
    history_id: int,
    session: Session = Depends(get_session),
    history_repository = Depends(dependencies.get_history_repository)
):
    item = history_repository.get_history_by_id(session=session, history_id=history_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"History with id {history_id} not found")

    return to_history_schema(item)


@router.get(
    "/url-id/{url_id}/",
    response_model=list[History],
    status_code=status.HTTP_200_OK,
    summary="Get history by url id"
)
async def get_history_by_url_id(
    url_id: int,
    session: Session = Depends(get_session),
    history_repository = Depends(dependencies.get_history_repository)
):
    items = history_repository.get_history_by_url_id(session=session, url_id=url_id)
    if not items:
        raise HTTPException(status_code=404, detail=f"History with URL id {url_id} not found")

    return [to_history_schema(item) for item in items]


@router.get(
    "/scraper-run-id/{scraper_run_id}/",
    response_model=History,
    status_code=status.HTTP_200_OK,
    summary="Get history by scraper run id"
)
async def get_history_by_scraper_run_id(
    scraper_run_id: int,
    session: Session = Depends(get_session),
    history_repository = Depends(dependencies.get_history_repository)
):
    item = history_repository.get_history_by_scraper_run_id(session=session, scraper_run_id=scraper_run_id)
    if not item:
        raise HTTPException(status_code=404, detail=f"History with Scraper run id {scraper_run_id} not found")

    return to_history_schema(item)