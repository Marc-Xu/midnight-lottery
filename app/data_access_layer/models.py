"""
Defines ORM models for the application.
"""

from sqlalchemy.orm import Mapped, mapped_column
from app.data_access_layer.database import Base


class Participant(Base):
    """
    ORM model for a participant entry.

    Attributes:
        id: Primary key.
        name: Participant name.
        email: Participant email.
    """

    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False, index=True)
    email: Mapped[str] = mapped_column(index=True)
