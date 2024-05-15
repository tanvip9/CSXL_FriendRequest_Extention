import { Component, OnInit } from '@angular/core';
import { FriendshipService } from '../../friendship.service';
import { User } from './friendship.model';
import { MatListModule } from '@angular/material/list';
import { MatButtonModule } from '@angular/material/button';
import { Route } from '@angular/router';
import { Profile, ProfileService } from '../../../profile/profile.service';

@Component({
  selector: 'app-send-request',
  templateUrl: './send-requests.component.html',
  styleUrls: ['./send-requests.component.css']
})
export class SendRequestsComponent implements OnInit {
  currentUserProfile: Profile | undefined;
  public static Route: Route = {
    path: 'send-request',
    component: SendRequestsComponent,
    title: 'Send Friend Request'
  };

  users: User[] = [];
  filteredUsers: User[] = [];
  searchBarQuery: string = '';

  constructor(
    private friendshipService: FriendshipService,
    private profileService: ProfileService
  ) {}

  ngOnInit(): void {
    this.loadUsers();
    this.subscribeToUserProfile();
    this.filteredUsers = this.users;
  }

  loadUsers(): void {
    this.friendshipService.getAllUsers().subscribe({
      next: (users) => {
        this.users = users;
        this.filteredUsers = users;
      },
      error: (error) => console.error('Error fetching users', error)
    });
  }

  subscribeToUserProfile(): void {
    this.profileService.profile$.subscribe((profile) => {
      this.currentUserProfile = profile;
    });
  }

  sendFriendRequest(receiver: User): void {
    this.friendshipService.sendFriendRequest(receiver.pid).subscribe({
      next: () => {
        alert(
          `Friend request sent to ${receiver.first_name} ${receiver.last_name}`
        );
        this.loadUsers();
      },
      error: (error) => console.error('Error sending friend request', error)
    });
  }

  onSearchBarQueryChange(query: string) {
    if (query.trim() !== '') {
      this.filteredUsers = this.users.filter((user) =>
        `${user.first_name} ${user.last_name}`
          .toLowerCase()
          .includes(query.toLowerCase())
      );
    } else {
      this.filteredUsers = this.users;
    }
  }
}
