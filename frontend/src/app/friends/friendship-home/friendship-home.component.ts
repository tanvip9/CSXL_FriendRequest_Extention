import { Component, OnInit } from '@angular/core';
import { FriendshipService } from '../friendship.service';
import { ProfileService } from '../../profile/profile.service';
import { Profile } from '../../../app/models.module';
import { Route } from '@angular/router';
import { FormBuilder, Validators } from '@angular/forms';

@Component({
  selector: 'app-friendship-home',
  templateUrl: './friendship-home.component.html',
  styleUrls: ['./friendship-home.component.css']
})
export class FriendshipHomeComponent implements OnInit {
  public static Route: Route = {
    path: 'friendship',
    component: FriendshipHomeComponent,
    title: 'Friendship XL'
  };
  currentUserProfile?: Profile;
  friendsCoworkingStatus: Array<{
    friend_pid: number;
    first_name: string;
    last_name: string;
    is_coworking: boolean;
  }> = [];
  pendingRequestsCount: number | undefined;

  coworkingForm = this.formBuilder.group({
    is_coworking: [false, Validators.required]
  });

  // Add a flag to track whether the initial value has been set
  private initialToggleSet = false;

  constructor(
    private friendshipService: FriendshipService,
    private profileService: ProfileService,
    private formBuilder: FormBuilder
  ) {
    // Listen to the current user's profile data
    this.profileService.profile$.subscribe({
      next: (profile) => {
        this.currentUserProfile = profile;
        
        // If there's a profile and the initial value hasn't been set, set the coworking status
        if (profile && !this.initialToggleSet) {
          this.coworkingForm.patchValue({ is_coworking: profile.is_coworking });
          this.fetchFriendsCoworkingStatus(profile.pid);
        }
      },
      error: (error) => console.error('Error fetching profile data', error)
    });
  }

  ngOnInit(): void {
    this.subscribeToUserProfile();
    this.fetchPendingRequestsCount();

    // Retrieve coworking status from localStorage on component initialization
    const storedCoworkingStatus = localStorage.getItem('coworkingStatus');
    if (storedCoworkingStatus !== null && !this.initialToggleSet) {
      this.coworkingForm.patchValue({
        is_coworking: JSON.parse(storedCoworkingStatus)
      });
      this.initialToggleSet = true;
    }
  }

  private subscribeToUserProfile(): void {
    this.profileService.profile$.subscribe({
      next: (profile) => {
        this.currentUserProfile = profile;
        if (profile && this.initialToggleSet) {
          // Set the form control value here
          this.coworkingForm
            .get('is_coworking')
            ?.setValue(profile.is_coworking, { emitEvent: false });
          this.fetchFriendsCoworkingStatus(profile.pid);
        }
      },
      error: (error) => console.error('Error in subscribeToUserProfile', error)
    });
  }

  fetchFriendsCoworkingStatus(pid: number): void {
    // Fetch friends' coworking status
    this.friendshipService.getFriendsCoworkingStatus(pid).subscribe({
      next: (statuses) => {
        this.friendsCoworkingStatus = statuses
          .filter((status) => status.is_coworking)
          .map((status) => ({
            friend_pid: status.pid,
            first_name: status.first_name,
            last_name: status.last_name,
            is_coworking: status.is_coworking
          }));
      },
      error: (error) =>
        console.error('Error fetching friends coworking status', error)
    });
  }

  toggleCoworkingStatus(): void {
    if (!this.currentUserProfile) return;

    const newStatus = !this.coworkingForm.get('is_coworking')?.value;

    this.friendshipService
      .updateCoworkingStatus(this.currentUserProfile.pid, newStatus)
      .subscribe({
        next: () => {
          // Update the form control to reflect the new state
          this.coworkingForm.patchValue({ is_coworking: newStatus });

          // Store coworking status in localStorage
          localStorage.setItem('coworkingStatus', JSON.stringify(newStatus));
          
          console.log('Coworking status updated successfully');
        },
        error: (error) =>
          console.error('Error updating coworking status', error)
      });
  }

  fetchPendingRequestsCount(): void {
    // Fetch the count of pending friend requests
    this.friendshipService.getReceivedRequestsCount().subscribe({
      next: (count) => (this.pendingRequestsCount = count),
      error: (error) =>
        console.error('Error fetching pending requests count', error)
    });
  }
}
