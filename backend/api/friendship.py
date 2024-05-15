from typing import List
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from backend.services.coworking.reservation import ReservationService
from ..services.friendship import FriendshipService
from ..models.user import User
from .authentication import registered_user

api = APIRouter(prefix="/api/friendships")
openapi_tags = {
    "name": "Friendships",
    "description": "Managing friendships and listing users.",
}


class CoworkingStatusForm(BaseModel):
    is_coworking: bool


class UserProfileUpdate(BaseModel):
    user_profile: User
    is_coworking: bool


@api.get("/users", response_model=list[User], tags=["Friendships"])
def list_users(
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    List all registered users excluding those who have already received a
    friend request from the current user and the user themselves.

    Returns:
        list[User]: A list of all eligible users.
    """
    return friendship_service.list_eligible_users(user.pid)


@api.post("/send-request/{receiver_id}", tags=["Friendships"])
def send_friend_request(
    receiver_id: int,
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    Send a friend request to another user.

    Args:
        receiver_id (int): The pid of the user to whom the friend request is being sent.
        user (User): The user sending the request, obtained from the dependency.

    Returns:
        A success message or an error message.
    """
    if user.pid == receiver_id:
        raise HTTPException(
            status_code=400, detail="Cannot send friend request to yourself."
        )

    try:
        friendship_service.create_friend_request(user.pid, receiver_id)
        return {"message": "Friend request sent successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@api.get("/requests/received", response_model=List[User], tags=["Friendships"])
def get_received_friend_requests(
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    Get all received friend requests for the authenticated user.

    Returns:
        list[FriendRequest]: A list of received friend requests.
    """
    try:
        received_requests = friendship_service.get_received_requests(user.pid)
        return received_requests
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/requests/received/count", response_model=int, tags=["Friendships"])
def get_received_friend_requests_count(
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    Get the count of received friend requests for the authenticated user.

    Returns:
        int: The number of received friend requests.
    """
    try:
        received_requests_count = friendship_service.get_received_requests_count(
            user.pid
        )
        return received_requests_count
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put("/accept/{request_id}", tags=["Friendships"])
def accept_friend_request(
    request_id: int,
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    Accept a friend request.

    Args:
        request_id (int): The ID of the friend request to accept.
        user (User): The user accepting the request, obtained from the dependency.

    Returns:
        A success message or an error message.
    """
    friendship_service.accept_request(request_id, user.pid)
    return {"message": "Friend request accepted successfully."}


@api.put("/reject/{request_id}", tags=["Friendships"])
def reject_friend_request(
    request_id: int,
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    Reject a friend request.

    Args:
        request_id (int): The ID of the friend request to reject.
        user (User): The user rejecting the request, obtained from the dependency.

    Returns:
        A success message or an error message.
    """
    try:
        friendship_service.reject_request(request_id, user.pid)
        return {"message": "Friend request rejected successfully."}
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/friends", response_model=list[User], tags=["Friendships"])
def get_friends(
    user: User = Depends(registered_user),
    friendship_service: FriendshipService = Depends(),
):
    """
    Get all friends for the authenticated user.

    Returns:
        list[User]: A list of friends for the authenticated user.
    """
    try:
        return friendship_service.get_friends(user.pid)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put("/update-coworking/{user_pid}", tags=["Coworking"])
def update_coworking_status(
    user_pid: int,
    coworking_status: CoworkingStatusForm,
    user: User = Depends(registered_user),
    reservation_service: ReservationService = Depends(),
):
    """
    Update coworking status for a user.
    """
    # pass just the profile into
    return reservation_service.update_coworking_status(
        user_pid, coworking_status.is_coworking
    )


@api.get(
    "/friends-coworking-status/{user_pid}",
    response_model=list[dict],
    tags=["Friendships"],
)
def get_friends_coworking_status(
    user_pid: int,
    friendship_service: FriendshipService = Depends(),
):
    """
    Get the coworking status of friends.

    Args:
        user_id (int): The ID of the user.
    """
    return friendship_service.get_friends_coworking_status(user_pid)
