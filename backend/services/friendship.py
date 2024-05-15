from fastapi import Depends

from sqlalchemy import AliasedReturnsRows, and_, exists, func, or_

from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from yaml import AliasEvent

from backend.entities import friendship_entity
from backend.entities.coworking.reservation_entity import ReservationEntity
from backend.models.coworking.reservation import ReservationState
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from ..database import db_session
from ..models.user import User
from ..entities.user_entity import UserEntity
from ..entities.friendship_entity import FriendshipEntity


class FriendshipService:
    def __init__(self, session: Session = Depends(db_session)):
        self._session = session

    def list_all_users(self) -> list[User]:
        """List all registered users."""
        users = self._session.query(UserEntity).all()
        return [user.to_model() for user in users]

    def create_friend_request(self, sender_id: int, receiver_id: int):
        """
        Create a new friend request.

        Args:
            sender_id (int): The ID of the user sending the friend request.
            receiver_id (int): The ID of the user receiving the friend request.
        """
        # Check for an existing friend request in both directions
        existing_request = (
            self._session.query(FriendshipEntity)
            .filter(
                (
                    (FriendshipEntity.sender == sender_id)
                    & (FriendshipEntity.receiver == receiver_id)
                )
                | (
                    (FriendshipEntity.sender == receiver_id)
                    & (FriendshipEntity.receiver == sender_id)
                )
            )
            .first()
        )

        if existing_request:
            raise Exception("A friend request already exists between these users.")

        # Create new friend request
        new_request = FriendshipEntity(
            sender=sender_id, receiver=receiver_id, status="requested"
        )
        self._session.add(new_request)
        self._session.commit()

    def get_received_requests(self, curr_user_id: int) -> list[User]:
        """
        Get all received friend requests for a user.

        Args:
            curr_user_id (int): The ID of the user receiving the friend requests.

        Returns:
            list[User]: A list of users who have sent friend requests.
        """
        # Query the friendships table for received friend requests
        requests = (
            self._session.query(FriendshipEntity)
            .filter(
                FriendshipEntity.receiver == curr_user_id,
                FriendshipEntity.status == "requested",
            )
            .options(joinedload(FriendshipEntity.sender_user))
            .all()
        )

        # Convert the results to User models
        users = [request.sender_user.to_model() for request in requests]
        return users

    def get_received_requests_count(self, curr_user_id: int) -> int:
        """
        Get the count of received friend requests for a user.

        Args:
            curr_user_id (int): The ID of the user receiving the friend requests.

        Returns:
            int: The number of received friend requests.
        """
        # Query the friendships table for the count of received friend requests
        count = (
            self._session.query(func.count())
            .filter(
                FriendshipEntity.receiver == curr_user_id,
                FriendshipEntity.status == "requested",
            )
            .scalar()
        )
        return count

    def accept_request(self, request_id: int, curr_user_id: int):
        """
        Accept a friend request.

        Args:
            request_id (int): The ID of the friend request to accept.
            curr_user_id (int): The ID of the user accepting the request.

        Raises:
            Exception: If the friend request is not found or the user is not the recipient.
        """
        # Fetch the friend request from the database
        request = (
            self._session.query(FriendshipEntity)
            .filter_by(sender=request_id, receiver=curr_user_id)
            .first()
        )

        # Check if the request exists and the user is the recipient
        if not request:
            raise ResourceNotFoundException("Friend request not found.")
            # elif request.receiver != curr_user_id:
            raise UserPermissionException("accept request", "this friend request")

        # Update the status of the friend request
        request.status = "accepted"
        self._session.commit()

    def reject_request(self, request_id: int, curr_user_id: int):
        """
        Reject a friend request.

        Args:
            request_id (int): The ID of the friend request to reject.
            curr_user_id (int): The ID of the user rejecting the request.

        Raises:
            Exception: If the friend request is not found or the user is not the recipient.
        """
        # Fetch the friend request from the database
        request = (
            self._session.query(FriendshipEntity)
            .filter_by(sender=request_id, receiver=curr_user_id)
            .first()
        )

        # Check if the request exists and the user is the recipient
        if not request:
            raise ResourceNotFoundException("Friend request not found.")
            # elif request.receiver != curr_user_id:
            raise UserPermissionException("reject request", "this friend request")

        # Update the status of the friend request
        request.status = "rejected"
        self._session.commit()

    def list_eligible_users(self, current_user_id: int) -> list[User]:
        """
        List all users excluding those who have already received a friend
        request from the current user and the user themselves.

        Args:
            current_user_id (int): The PID of the current user.

        Returns:
            list[User]: A list of all eligible users.
        """
        # Query to find users who have not received a friend request from the current user
        # and are not the current user.
        eligible_users = (
            self._session.query(UserEntity)
            .filter(UserEntity.pid != current_user_id)
            .filter(
                ~exists().where(
                    or_(
                        and_(
                            FriendshipEntity.sender == current_user_id,
                            FriendshipEntity.receiver == UserEntity.pid,
                        ),
                        and_(
                            FriendshipEntity.sender == UserEntity.pid,
                            FriendshipEntity.receiver == current_user_id,
                        ),
                    )
                )
            )
            .all()
        )
        return [user.to_model() for user in eligible_users]

    def get_friends(self, curr_user_id: int) -> list[User]:
        """
        Get all friends for a user.

        Args:
            curr_user_id (int): The ID of the user for whom to fetch friends.

        Returns:
            list[User]: A list of friends for the specified user.
        """
        # Query the friendships table for accepted friend requests
        friends_query = (
            self._session.query(FriendshipEntity)
            .filter(
                or_(
                    and_(
                        FriendshipEntity.sender == curr_user_id,
                        FriendshipEntity.status == "accepted",
                    ),
                    and_(
                        FriendshipEntity.receiver == curr_user_id,
                        FriendshipEntity.status == "accepted",
                    ),
                )
            )
            .options(
                joinedload(FriendshipEntity.sender_user),
                joinedload(FriendshipEntity.receiver_user),
            )
        )

        friends = []
        for friend_rel in friends_query:
            # Determine which user is the friend
            if friend_rel.sender == curr_user_id:
                # Current user is the sender, so the friend is the receiver
                friend = (
                    friend_rel.receiver_user.to_model()
                    if friend_rel.receiver_user.id != curr_user_id
                    else None
                )
            else:
                # Current user is the receiver, so the friend is the sender
                friend = (
                    friend_rel.sender_user.to_model()
                    if friend_rel.sender_user.id != curr_user_id
                    else None
                )

            if friend:
                friends.append(friend)

        return friends

    def get_friends_coworking_status(self, user_pid: int) -> list[dict]:
        # Join the UserEntity with FriendshipEntity where the user is either the sender or receiver
        # and the friendship status is accepted. Also, join with ReservationEntity to check the check-in status.
        friends_query = (
            self._session.query(UserEntity)
            .join(
                FriendshipEntity,
                or_(
                    and_(
                        UserEntity.pid == FriendshipEntity.sender,
                        FriendshipEntity.receiver == user_pid,
                    ),
                    and_(
                        UserEntity.pid == FriendshipEntity.receiver,
                        FriendshipEntity.sender == user_pid,
                    ),
                ),
            )
            .filter(FriendshipEntity.status == "accepted")
        )

        # Execute the query and fetch the results
        friends = friends_query.all()

        # Convert the results into a list of dictionaries
        friends_coworking_status = [
            {
                "friend_pid": friend.pid,
                "first_name": friend.first_name,
                "last_name": friend.last_name,
                "is_coworking": friend.is_coworking,
            }
            for friend in friends
            if friend.pid != user_pid  # Exclude the current user's own record
        ]

        return friends_coworking_status
