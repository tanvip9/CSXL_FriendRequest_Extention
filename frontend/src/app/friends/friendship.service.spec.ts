import { TestBed } from '@angular/core/testing';

import { FriendshipService } from './friendship.service';

describe('SendRequestService', () => {
  let service: FriendshipService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(FriendshipService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
