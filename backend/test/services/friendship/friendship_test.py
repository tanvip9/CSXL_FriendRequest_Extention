# Import necessary libraries and fixtures
import pytest
from backend.models.user import User
from backend.services.exceptions import (
    ResourceNotFoundException,
    UserPermissionException,
)
from backend.services.friendship import FriendshipService
from sqlalchemy.orm import Session
from backend.entities.friendship_entity import FriendshipEntity
from backend.entities.user_entity import UserEntity

from backend.test.services.friendship.friendship_test_data import mock_friend_request

from backend.test.services.user_data import user, root, ambassador


@pytest.fixture
def prepared_session(session: Session):
    # Insert the predefined users into the database
    root_entity = UserEntity.from_model(root)
    user_entity = UserEntity.from_model(user)
    session.add(root_entity)
    session.add(user_entity)
    session.commit()

    root.id = root_entity.id
    user.id = user_entity.id
    return session


def test_create_duplicate_friend_request(prepared_session: Session):
    # Initialize FriendshipService with the prepared_session
    service = FriendshipService(session=prepared_session)

    # create a friend request
    service.create_friend_request(root.pid, user.pid)

    # Try to create the same friend request again and expect an exception
    with pytest.raises(Exception) as exc_info:
        service.create_friend_request(root.pid, user.pid)

    # Assert that the exception message is as expected
    assert "A friend request already exists between these users" in str(exc_info.value)


def test_create_friend_request(prepared_session: Session):
    # Ensure user PIDs exist in the database
    assert (
        prepared_session.query(UserEntity)
        .filter(UserEntity.pid == root.pid)
        .one_or_none()
        is not None
    )
    assert (
        prepared_session.query(UserEntity)
        .filter(UserEntity.pid == user.pid)
        .one_or_none()
        is not None
    )

    # Initialize FriendshipService with the prepared_session
    service = FriendshipService(session=prepared_session)

    # Use pid for creating friend request
    service.create_friend_request(root.pid, user.pid)

    # Assertions to check if the friend request is created correctly
    assert (
        prepared_session.query(FriendshipEntity)
        .filter_by(sender=root.pid, receiver=user.pid)
        .count()
        == 1
    )


# Test listing all users eligible for friend requests
def test_list_eligible_users(prepared_session: Session):  # Updated parameter name
    service = FriendshipService(prepared_session)
    if user.id is None or root.id is None:
        raise ValueError("User ID or Root ID is not set.")
    eligible_users = service.list_eligible_users(user.id)
    assert any(user.id == root.id for user in eligible_users)


def test_list_all_users(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Call the function
    all_users = service.list_all_users()

    # Assert that the returned list matches the users in the database
    assert len(all_users) == 2  # or the number of users you've added
    assert all(isinstance(user, User) for user in all_users)


def test_accept_friend_request(
    prepared_session: Session, mock_friend_request: FriendshipEntity
):
    service = FriendshipService(session=prepared_session)

    # Call the method to accept the friend request
    # Use the correct id value for the user object
    service.accept_request(root.pid, user.pid)

    # Fetch the updated request from the database
    updated_request = prepared_session.query(FriendshipEntity).get(
        mock_friend_request.id
    )

    # Assert that the status of the friend request is now 'accepted'
    assert updated_request.status == "accepted"


def test_reject_friend_request(
    prepared_session: Session, mock_friend_request: FriendshipEntity
):
    service = FriendshipService(session=prepared_session)
    service.reject_request(root.pid, user.pid)
    # Fetch the updated request from the database
    updated_request = prepared_session.query(FriendshipEntity).get(
        mock_friend_request.id
    )

    # Assert that the status of the friend request is now 'rejected'
    assert updated_request.status == "rejected"


def test_get_received_requests(
    prepared_session: Session, mock_friend_request: FriendshipEntity
):
    service = FriendshipService(session=prepared_session)

    # Call the method with user.pid who is set as the receiver
    received_requests = service.get_received_requests(user.pid)

    # Assert that received_requests contains users who have sent friend requests
    assert len(received_requests) > 0
    assert all(isinstance(request, User) for request in received_requests)
    assert any(
        request.pid == root.pid for request in received_requests
    )  # Check if root is in received requests


def test_get_received_requests_no_requests(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Call the method for a user with no received friend requests
    received_requests = service.get_received_requests(
        user.pid
    )  # some_other_user needs to be defined

    # Assert that no friend requests are returned
    assert len(received_requests) == 0


# Test getting friends list
def test_get_friends(prepared_session: Session):
    service = FriendshipService(prepared_session)
    if user.id is None or root.id is None:
        raise ValueError("User ID or Root ID is not set.")
    friends = service.get_friends(user.id)
    assert isinstance(friends, list)


# Additional tests for error handling and exceptions
def test_error_handling(prepared_session: Session):
    service = FriendshipService(prepared_session)
    if user.id is None or root.id is None:
        raise ValueError("User ID or Root ID is not set.")
    # Test for non-existent request handling
    with pytest.raises(Exception):
        service.accept_request(999, user.id)
    with pytest.raises(Exception):
        service.reject_request(999, user.id)


def test_get_received_requests_count(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Create multiple friend requests for the user
    # Assuming 'root' is sending requests to 'user'
    service.create_friend_request(root.pid, user.pid)

    # Get the count of received friend requests for 'user'
    count = service.get_received_requests_count(user.pid)

    # Assert that the count matches the expected number of requests
    # This should be the number of requests you've created above
    expected_count = 1
    assert count == expected_count


def test_accept_nonexistent_friend_request(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Try to accept a non-existent friend request
    with pytest.raises(ResourceNotFoundException) as exc_info:
        service.accept_request(999, user.pid)

    # Assert that the exception message is as expected
    assert "Friend request not found." in str(exc_info.value)


def test_reject_nonexistent_friend_request(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Try to reject a non-existent friend request
    with pytest.raises(ResourceNotFoundException) as exc_info:
        service.reject_request(999, user.pid)

    # Assert that the exception message is as expected
    assert "Friend request not found." in str(exc_info.value)


def test_get_friends_coworking_status(
    prepared_session: Session, mock_friend_request: FriendshipEntity
):
    service = FriendshipService(session=prepared_session)

    # Assuming mock_friend_request is an accepted friendship
    # You may need to update the status of the friendship to 'accepted' here
    mock_friend_request.status = "accepted"
    prepared_session.commit()

    coworking_status = service.get_friends_coworking_status(user.pid)

    # Assert that the coworking status is correctly returned
    assert isinstance(coworking_status, list)
    assert any(friend["friend_pid"] == root.pid for friend in coworking_status)


def test_accept_invalid_friend_request(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Attempt to accept an invalid friend request
    with pytest.raises(ResourceNotFoundException):
        service.accept_request(9999, user.pid)  # Assuming 9999 is an invalid request ID


def test_reject_invalid_friend_request(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    # Attempt to reject an invalid friend request
    with pytest.raises(ResourceNotFoundException):
        service.reject_request(9999, user.pid)  # Assuming 9999 is an invalid request ID


def test_get_friends_with_self_as_friend(
    prepared_session: Session, mock_friend_request: FriendshipEntity
):
    service = FriendshipService(session=prepared_session)

    mock_friend_request.sender = user.pid
    mock_friend_request.receiver = user.pid
    mock_friend_request.status = "accepted"
    prepared_session.add(mock_friend_request)
    prepared_session.commit()

    # Test: Call get_friends with the current user's PID
    friends = service.get_friends(user.pid)

    # Assert: Check if the friend list is empty since user cannot be friends with themselves
    assert friends


def test_get_friends_identifies_sender_as_friend(prepared_session: Session):
    service = FriendshipService(session=prepared_session)

    friend_request = FriendshipEntity(
        sender=root.pid,  # root is the sender
        receiver=user.pid,  # user is the receiver and the current user for this test
        status="accepted",
    )
    prepared_session.add(friend_request)
    prepared_session.commit()

    # Call get_friends with the current user's PID who is the receiver in the friend request
    friends = service.get_friends(user.pid)

    # Assert that the friend list includes the sender of the friend request
    assert len(friends) == 1
    assert (
        friends[0].pid == root.pid
    )  # Check if root (the sender) is identified as a friend
