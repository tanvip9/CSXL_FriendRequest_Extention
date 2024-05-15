# tests/friendship_test_data.py

import pytest
from sqlalchemy.orm import Session
from backend.entities.friendship_entity import FriendshipEntity

# Importing predefined users from your mock data
from backend.test.services.user_data import root, user


@pytest.fixture
def mock_friend_request(session: Session):
    # Create a mock friend request between predefined users
    friend_request = FriendshipEntity(
        sender=root.pid, receiver=user.pid, status="requested"
    )
    session.add(friend_request)
    session.commit()
    return friend_request
