"""
Defines ORM models for the application.
"""

from datetime import datetime, date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


from app.data_access_layer.database import Base


class Participant(Base):
    """
    ORM model for a participant entry.

    Attributes:
        id: Primary key.
        name: Participant name.
        email: Participant email.
    """

    __tablename__ = "participants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(index=True)


class Draw(Base):
    """
    ORM model for a lottery draw.

    Attributes:
        id: Primary key.
        draw_date: Unique date of the draw.
        winner_id: Foreign key referencing the winning participant.
        winner: Relationship to the Participant object who won.
    """

    __tablename__ = "draws"

    id: Mapped[int] = mapped_column(primary_key=True)
    draw_date: Mapped[date] = mapped_column(unique=True, index=True)
    winner_id: Mapped[int | None] = mapped_column(ForeignKey("participants.id"))

    winner: Mapped[Participant | None] = relationship()


class Ballot(Base):
    """
    ORM model for a ballot entry.

    Attributes:
        id: Primary key.
        participant_id: Foreign key referencing the participant.
        draw_id: Foreign key referencing the draw.
        timestamp: Time the ballot was submitted.
        participant: Relationship to the Participant object.
        draw: Relationship to the Draw object.
    """

    __tablename__ = "ballots"

    id: Mapped[int] = mapped_column(primary_key=True)
    participant_id: Mapped[int] = mapped_column(ForeignKey("participants.id"))
    draw_id: Mapped[int] = mapped_column(ForeignKey("draws.id"))
    timestamp: Mapped[datetime] = mapped_column(default=datetime.now())

    participant: Mapped[Participant] = relationship()
    draw: Mapped[Draw] = relationship()
