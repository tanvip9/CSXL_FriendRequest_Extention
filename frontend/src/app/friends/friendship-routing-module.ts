import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SendRequestsComponent } from './requests/send-requests/send-requests.component';
import { FriendshipHomeComponent } from './friendship-home/friendship-home.component';
import { ViewRequestsComponent } from './requests/view-requests/view-requests.component';
import { ViewFriendsComponent } from './requests/view-friends/view-friends.component';

const routes: Routes = [
  SendRequestsComponent.Route,
  FriendshipHomeComponent.Route,
  ViewRequestsComponent.Route,
  ViewFriendsComponent.Route
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class FriendshipRoutingModule {}
