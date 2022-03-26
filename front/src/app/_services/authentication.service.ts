import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { BehaviorSubject, Observable } from 'rxjs';
import { map } from 'rxjs/operators';

const api_url = "https://localhost:80"

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
  private currentUserSubject: BehaviorSubject<any>;
  public currentUser: Observable<any>;

  constructor(private http: HttpClient) {
    localStorage.setItem('currentUser', 'dan');
    const currentUser = localStorage.getItem('currentUser') || '';

    console.log("AuthenticationService.constructor");
    console.log(currentUser);

    this.currentUserSubject = new BehaviorSubject<string>(currentUser);


    this.currentUser = this.currentUserSubject.asObservable();
  }

  public get currentUserValue() {
    console.log("AuthenticationService -> get currentUservalue");
    return this.currentUserSubject.value;
  }

  login(username: string, password: string) {
    return this.http.post<any>(
      `${api_url}/users/authenticate`, { username, password }
    )
      .pipe(map(user => {
        // store user details and jwt token in local storage to keep user logged in between page refreshes
        localStorage.setItem('currentUser', JSON.stringify(user));
        this.currentUserSubject.next(user);
        return user;
      }));
  }

  logout() {
    // remove user from local storage and set current user to null
    localStorage.removeItem('currentUser');
    this.currentUserSubject.next(null);
  }
}
