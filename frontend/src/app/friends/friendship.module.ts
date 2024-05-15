import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';

import { MatTableModule } from '@angular/material/table';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';

import { FriendshipRoutingModule } from './friendship-routing-module';
import { FriendshipHomeComponent } from './friendship-home/friendship-home.component';
import { SendRequestsComponent } from './requests/send-requests/send-requests.component';
import { ViewRequestsComponent } from './requests/view-requests/view-requests.component';
import { ViewFriendsComponent } from './requests/view-friends/view-friends.component';
import { MatCardModule } from '@angular/material/card';
import { SharedModule } from '../shared/shared.module';
import { MatSlideToggleModule } from '@angular/material/slide-toggle';

@NgModule({
  declarations: [
    FriendshipHomeComponent,
    SendRequestsComponent,
    ViewRequestsComponent,
    ViewFriendsComponent
  ],
  imports: [
    CommonModule,
    FriendshipRoutingModule,
    MatTabsModule,
    MatTableModule,
    MatDialogModule,
    MatButtonModule,
    MatListModule,
    MatAutocompleteModule,
    MatCardModule,
    FormsModule,
    ReactiveFormsModule,
    MatButtonModule,
    SharedModule,
    MatSlideToggleModule
  ]
})
export class FriendshipModule {}
