"""
Defines all /draws endpoints via APIRouter.
"""

from typing import List
from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from app.business_logic.draw_service import DrawService
from app.data_access_layer.database import get_db
from app.api.v1.schemas.draw import (
    DrawCreate,
    Draw,
)

router = APIRouter()


def get_draw_service(db: Session = Depends(get_db)) -> DrawService:
    """
    Dependency to provide a DrawService instance for use cases.
    """
    return DrawService(db=db)


@router.post("/", response_model=Draw, summary="Create draw")
def create_draw(
    payload: DrawCreate,
    service: DrawService = Depends(get_draw_service),
) -> Draw:
    """
    Create a new draw using service layer.
    """
    return service.create(payload.model_dump(exclude_unset=True))


@router.get("/", response_model=List[Draw], summary="List draws")
def list_draws(
    skip: int = 0,
    limit: int = Query(10, ge=1, le=100),
    service: DrawService = Depends(get_draw_service),
) -> List[Draw]:
    """
    List draws with pagination via service.
    """
    return service.list_all(skip=skip, limit=limit)


@router.get("/{draw_id}", response_model=Draw, summary="Get draw by ID")
def get_draw(
    draw_id: int,
    service: DrawService = Depends(get_draw_service),
) -> Draw:
    """
    Fetch a single draw by ID via service.
    """
    return service.get(draw_id)


@router.delete("/{draw_id}", response_model=Draw, summary="Delete draw")
def delete_draw(
    draw_id: int,
    service: DrawService = Depends(get_draw_service),
) -> Draw:
    """
    Delete a draw via service.
    """
    return service.delete(draw_id)
