import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable, catchError, tap } from 'rxjs';
import { User } from './requests/send-requests/friendship.model';
import { FriendRequest } from './requests/view-requests/friend_request.model';

@Injectable({
  providedIn: 'root'
})
export class FriendshipService {
  private usersUrl = '/api/friendships/users';

  constructor(private http: HttpClient) {}

  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.usersUrl);
  }

  sendFriendRequest(receiverId: number): Observable<any> {
    const requestUrl = `/api/friendships/send-request/${receiverId}`;
    return this.http.post(requestUrl, {});
  }

  getReceivedRequests(): Observable<FriendRequest[]> {
    return this.http
      .get<FriendRequest[]>('/api/friendships/requests/received')
      .pipe(
        catchError((error) => {
          console.error('Error fetching received requests', error);
          throw error;
        })
      );
  }

  getReceivedRequestsCount(): Observable<number> {
    return this.http
      .get<number>('/api/friendships/requests/received/count')
      .pipe(
        catchError((error) => {
          console.error('Error fetching received requests count', error);
          throw error;
        })
      );
  }

  acceptRequest(requestId: number): Observable<any> {
    return this.http
      .put(`/api/friendships/accept/${requestId}`, {})
      .pipe(tap((response) => console.log('Server Response:', response)));
  }

  rejectRequest(requestId: number): Observable<any> {
    return this.http.put(`/api/friendships/reject/${requestId}`, {});
  }

  getFriends(): Observable<User[]> {
    return this.http.get<User[]>('/api/friendships/friends').pipe(
      catchError((error) => {
        console.error('Error fetching Friends', error);
        throw error;
      })
    );
  }

  updateCoworkingStatus(user_pid: number, status: boolean): Observable<any> {
    return this.http.put(`/api/friendships/update-coworking/${user_pid}`, {
      is_coworking: status
    });
  }

  getFriendsCoworkingStatus(user_pid: number): Observable<User[]> {
    return this.http.get<User[]>(
      `/api/friendships/friends-coworking-status/${user_pid}`
    );
  }
}
