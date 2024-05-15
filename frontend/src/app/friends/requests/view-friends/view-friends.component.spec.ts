import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ViewFriendsComponent } from './view-friends.component';

describe('ViewFriendsComponent', () => {
  let component: ViewFriendsComponent;
  let fixture: ComponentFixture<ViewFriendsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ViewFriendsComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(ViewFriendsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
