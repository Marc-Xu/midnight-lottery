"""
Defines all /ballots endpoints via APIRouter.
"""

from typing import List
from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from app.business_logic.ballot_service import BallotService
from app.data_access_layer.database import get_db
from app.api.v1.schemas.ballot import (
    BallotCreate,
    Ballot,
)

router = APIRouter()


def get_ballot_service(db: Session = Depends(get_db)) -> BallotService:
    """
    Dependency to provide a BallotService instance for use cases.
    """
    return BallotService(db=db)


@router.post("/", response_model=Ballot, summary="Create ballot")
def create_ballot(
    payload: BallotCreate,
    service: BallotService = Depends(get_ballot_service),
) -> Ballot:
    """
    Create a new ballot using service layer.
    """
    return service.create(payload.model_dump(exclude_unset=True))


@router.get("/", response_model=List[Ballot], summary="List ballots")
def list_ballots(
    skip: int = 0,
    limit: int = Query(10, ge=1, le=100),
    service: BallotService = Depends(get_ballot_service),
) -> List[Ballot]:
    """
    List ballots with pagination via service.
    """
    return service.list_all(skip=skip, limit=limit)


@router.get("/{ballot_id}", response_model=Ballot, summary="Get ballot by ID")
def get_ballot(
    ballot_id: int,
    service: BallotService = Depends(get_ballot_service),
) -> Ballot:
    """
    Fetch a single ballot by ID via service.
    """
    return service.get(ballot_id)


@router.delete("/{ballot_id}", response_model=Ballot, summary="Delete ballot")
def delete_ballot(
    ballot_id: int,
    service: BallotService = Depends(get_ballot_service),
) -> Ballot:
    """
    Delete a ballot via service.
    """
    return service.delete(ballot_id)
