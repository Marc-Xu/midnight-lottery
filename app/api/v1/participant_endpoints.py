"""
Defines all /participants endpoints via APIRouter.
"""

from typing import List
from fastapi import APIRouter
from fastapi import Depends, Query
from sqlalchemy.orm import Session
from app.business_logic.participant_service import ParticipantService
from app.data_access_layer.database import get_db
from app.api.v1.schemas.participant import (
    ParticipantCreate,
    ParticipantUpdate,
    Participant,
)


router = APIRouter()


def get_participant_service(db: Session = Depends(get_db)) -> ParticipantService:
    """
    Dependency to provide a ParticipantService instance for use cases.
    """
    return ParticipantService(db)


@router.post("/", response_model=Participant, summary="Create participant")
def create_participant(
    payload: ParticipantCreate,
    service: ParticipantService = Depends(get_participant_service),
) -> Participant:
    """
    Create a new participant using service layer.
    """
    return service.create(payload.model_dump(exclude_unset=True))


@router.get("/", response_model=List[Participant], summary="List participants")
def list_participants(
    skip: int = 0,
    limit: int = Query(10, ge=1, le=100),
    service: ParticipantService = Depends(get_participant_service),
) -> List[Participant]:
    """
    List participants with pagination via service.
    """
    return service.list_all(skip=skip, limit=limit)


@router.get(
    "/{participant_id}", response_model=Participant, summary="Get participant by ID"
)
def get_participant(
    participant_id: int,
    service: ParticipantService = Depends(get_participant_service),
) -> Participant:
    """
    Fetch a single participant by ID via service.
    """
    return service.get(participant_id)


@router.patch(
    "/{participant_id}", response_model=Participant, summary="Update participant"
)
def patch_participant(
    participant_id: int,
    payload: ParticipantUpdate,
    service: ParticipantService = Depends(get_participant_service),
) -> Participant:
    """
    Partially update a participant via service.
    """
    return service.update(participant_id, payload.model_dump(exclude_unset=True))


@router.delete(
    "/{participant_id}", response_model=Participant, summary="Delete participant"
)
def delete_participant(
    participant_id: int,
    service: ParticipantService = Depends(get_participant_service),
) -> Participant:
    """
    Delete a participant via service.
    """
    return service.delete(participant_id)
