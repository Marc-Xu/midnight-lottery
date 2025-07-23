"""
Pydantic models for request validation and response serialization.
"""

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class DrawBase(BaseModel):
    """
    Shared properties of a draw.

    Attributes:
        winner_id: ID of the winner.
    """

    winner_id: int | None = Field(None, description="Winner's ID")


class DrawCreate(DrawBase):
    """Properties for creating a new draw."""

    pass


class Draw(DrawBase):
    """
    Properties returned in API responses.

    Attributes:
        id: Unique identifier.
        draw_date: ID of the draw.
    """

    id: int = Field(..., description="Unique ID")
    draw_date: datetime = Field(..., description="Date of the draw")
    model_config = ConfigDict(from_attributes=True)
