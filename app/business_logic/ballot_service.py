"""
Business-logic layer orchestrating ballot use-cases.
"""

from typing import Any
from datetime import datetime

from sqlalchemy.orm import Session

from app.business_logic.draw_service import DrawService
from app.business_logic.general_service import GeneralService
from app.data_access_layer.models import Ballot
from app.exceptions import NotFoundError


class BallotService(GeneralService[Ballot]):
    """
    Orchestrates business rules and use-cases for Ballot.
    """

    def __init__(self, db: Session):
        super().__init__(db, Ballot)

    def create(self, ballot_data: dict[str, Any]) -> Ballot:
        draw_service = DrawService(db=self.db)
        date = datetime.now().date()
        try:
            daily_draw = draw_service.get_by_attributes(attributes={"draw_date": date})
        except NotFoundError:
            raise NotFoundError(
                f"A lottery with date '{date}' has not been created yet."
            )
        ballot_data["draw_id"] = daily_draw[0].id
        return self.repo.add(**ballot_data)
