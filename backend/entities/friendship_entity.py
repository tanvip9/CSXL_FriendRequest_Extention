"""Definition of SQLAlchemy table-backed object mapping entity for Friendships."""

from sqlalchemy import Integer, String, TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, backref
from typing import Self
from .entity_base import EntityBase
from .user_entity import UserEntity


class FriendshipEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `friendships` table"""

    __tablename__ = "friendships"

    # Unique ID for the friendship entry
    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    # User ID of the first user
    sender: Mapped[int] = mapped_column(Integer, ForeignKey("user.pid"), nullable=False)

    # User ID of the second user
    receiver: Mapped[int] = mapped_column(
        Integer, ForeignKey("user.pid"), nullable=False
    )

    # Status of the friendship
    status: Mapped[str] = mapped_column(String(10), nullable=False)

    # Relationship back to UserEntity for sender
    sender_user: Mapped["UserEntity"] = relationship(
        "UserEntity", backref=backref("sent_friend_requests"), foreign_keys=[sender]
    )

    # Relationship back to UserEntity for receiver
    receiver_user: Mapped["UserEntity"] = relationship(
        "UserEntity",
        backref=backref("received_friend_requests"),
        foreign_keys=[receiver],
    )
