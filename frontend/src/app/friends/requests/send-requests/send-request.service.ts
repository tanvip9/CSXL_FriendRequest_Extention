import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { User } from './friendship.model';

@Injectable({
  providedIn: 'root'
})
export class SendRequestService {
  private usersUrl = '/api/friendships/users';

  constructor(private http: HttpClient) {}

  getAllUsers(): Observable<User[]> {
    return this.http.get<User[]>(this.usersUrl);
  }
}
