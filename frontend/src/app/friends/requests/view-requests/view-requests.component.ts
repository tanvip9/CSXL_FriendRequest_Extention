import { Component, OnInit } from '@angular/core';
import { FriendshipService } from '../../friendship.service';
import { FriendRequest } from './friend_request.model';
import { Route, Router } from '@angular/router';
import { Observable, catchError } from 'rxjs';
import { AuthenticationService } from 'src/app/authentication.service';

@Component({
  selector: 'app-view-requests',
  templateUrl: './view-requests.component.html',
  styleUrls: ['./view-requests.component.css']
})
export class ViewRequestsComponent implements OnInit {
  receivedRequests: FriendRequest[] = [];
  public static Route: Route = {
    path: 'view-requests',
    component: ViewRequestsComponent,
    title: 'View Friend Requests'
  };
  receivedRequests$: Observable<FriendRequest[]> | undefined;

  constructor(
    private authService: AuthenticationService,
    private friendshipService: FriendshipService
  ) {}

  ngOnInit(): void {
    this.receivedRequests$ = this.friendshipService.getReceivedRequests().pipe(
      catchError((error) => {
        console.error('Error fetching friend requests', error);
        return [];
      })
    );

    this.receivedRequests$.subscribe(
      (requests) => (this.receivedRequests = requests)
    );
  }

  acceptRequest(requestId: number): void {
    window.alert('Accepted Friend Request');
    this.friendshipService.acceptRequest(requestId).subscribe({
      next: () => {},
      error: (error) => {
        console.error('Error accepting friend request', error);
      }
    });
    this.ngOnInit();
  }

  rejectRequest(requestId: number): void {
    window.alert('Rejected Friend Request');
    this.friendshipService.rejectRequest(requestId).subscribe({
      next: () => {},
      error: (error) => console.error('Error rejecting request', error)
    });
    this.ngOnInit();
  }
}
