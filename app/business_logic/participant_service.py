"""
Business-logic layer orchestrating participant use-cases.
"""

from typing import Any

from sqlalchemy.orm import Session

from app.business_logic.general_service import GeneralService
from app.data_access_layer.models import Participant
from app.exceptions import ValidationError


class ParticipantService(GeneralService[Participant]):
    """
    Orchestrates business rules and use-cases for Participant.
    """

    def __init__(self, db: Session):
        super().__init__(db, Participant)

    def create(self, participant_data: dict[str, Any]) -> Participant:
        # Business rule: Participant email must be unique
        if self.repo.find_by(email=participant_data["email"]):
            raise ValidationError(
                f"A participant with email '{participant_data["email"]}' already exists."
            )
        return self.repo.add(**participant_data)
