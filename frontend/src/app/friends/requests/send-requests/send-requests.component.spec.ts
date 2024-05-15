import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SendRequestsComponent } from './send-requests.component';

describe('SendRequestsComponent', () => {
  let component: SendRequestsComponent;
  let fixture: ComponentFixture<SendRequestsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SendRequestsComponent]
    }).compileComponents();

    fixture = TestBed.createComponent(SendRequestsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
