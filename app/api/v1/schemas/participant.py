"""
Pydantic models for request validation and response serialization.
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class ParticipantBase(BaseModel):
    """
    Shared properties of a participant.

    Attributes:
        name: Name of the participant.
        email: Email of the participant.
    """

    name: str = Field(..., description="Participant name")
    email: str = Field(..., description="Participant email")


class ParticipantCreate(ParticipantBase):
    """Properties for creating a new participant."""

    pass


class Participant(ParticipantBase):
    """
    Properties returned in API responses.

    Attributes:
        id: Unique identifier.
    """

    id: int = Field(..., description="Unique ID")
    model_config = ConfigDict(from_attributes=True)


class ParticipantUpdate(ParticipantBase):
    """
    Properties for updating an existing participant. All fields are optional.
    """

    name: Optional[str] = Field(None, description="Participant name")
    email: Optional[str] = Field(None, description="Participant email")

    model_config = ConfigDict(from_attributes=True)
