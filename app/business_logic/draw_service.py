"""
Business-logic layer orchestrating draw use-cases.
"""

from typing import Any
from datetime import datetime

from sqlalchemy.orm import Session

from app.business_logic.general_service import GeneralService
from app.data_access_layer.models import Draw
from app.exceptions import ValidationError


class DrawService(GeneralService[Draw]):
    """
    Orchestrates business rules and use-cases for Draw.
    """

    def __init__(self, db: Session):
        super().__init__(db, Draw)

    def create(self, draw_data: dict[str, Any]) -> Draw:
        # Business rule: One draw per day
        draw_data["draw_date"] = datetime.now().date()
        if self.repo.find_by(draw_date=draw_data["draw_date"]):
            raise ValidationError(
                f"A draw with date '{draw_data["draw_date"]}' already exists."
            )
        return self.repo.add(**draw_data)
