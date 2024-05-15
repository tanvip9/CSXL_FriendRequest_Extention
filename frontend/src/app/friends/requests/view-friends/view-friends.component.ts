import { Component, OnInit } from '@angular/core';
import { User } from '../../requests/send-requests/friendship.model';
import { FriendshipService } from '../../friendship.service';
import { Route } from '@angular/router';
import { Observable } from 'rxjs';

@Component({
  selector: 'app-view-friends',
  templateUrl: './view-friends.component.html',
  styleUrls: ['./view-friends.component.css']
})
export class ViewFriendsComponent implements OnInit {
  friends: User[] = [];
  public static Route: Route = {
    path: 'view-friends',
    component: ViewFriendsComponent,
    title: 'View Friends'
  };

  friends$: Observable<User[]> | undefined;
  filteredFriends: User[] = [];
  searchBarQuery: string = '';

  constructor(private friendshipService: FriendshipService) {}

  ngOnInit(): void {
    this.loadFriends();
  }

  loadFriends(): void {
    this.friends$ = this.friendshipService.getFriends();
    this.friends$.subscribe((friend_request) => {
      this.friends = friend_request;
      this.filteredFriends = friend_request;
    });
  }

  onSearchBarQueryChange(query: string) {
    if (query.trim() !== '') {
      this.filteredFriends = this.friends.filter((friend) =>
        `${friend.first_name} ${friend.last_name}`
          .toLowerCase()
          .includes(query.toLowerCase())
      );
    } else {
      this.filteredFriends = this.friends;
    }
  }
}
