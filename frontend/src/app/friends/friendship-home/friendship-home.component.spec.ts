import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FriendshipHomeComponent } from './friendship-home.component';

describe('FriendshipHomeComponent', () => {
  let component: FriendshipHomeComponent;
  let fixture: ComponentFixture<FriendshipHomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FriendshipHomeComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(FriendshipHomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
