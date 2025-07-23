"""
Pydantic models for request validation and response serialization.
"""

from pydantic import BaseModel, Field, ConfigDict


class BallotBase(BaseModel):
    """
    Shared properties of a ballot.

    Attributes:
        participant_id: ID of the participant.
    """

    participant_id: int = Field(..., description="Participant's ID")


class BallotCreate(BallotBase):
    """Properties for creating a new ballot."""

    pass


class Ballot(BallotBase):
    """
    Properties returned in API responses.

    Attributes:
        id: Unique identifier.
        draw_id: ID of the draw.
    """

    id: int = Field(..., description="Unique ID")
    draw_id: int = Field(..., description="Draw's ID")
    model_config = ConfigDict(from_attributes=True)
