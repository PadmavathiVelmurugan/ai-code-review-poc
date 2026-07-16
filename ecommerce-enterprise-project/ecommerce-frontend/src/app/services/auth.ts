import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AuthService {

  private apiUrl = 'http://localhost:8080/api/auth';

  constructor(private http: HttpClient) {}

  register(user: any) {
    return this.http.post(
      `${this.apiUrl}/register`,
      user
    );
  }

  login(credentials: any) {
    return this.http.post(
      `${this.apiUrl}/login`,
      credentials,
      {
        responseType: 'text'
      }
    );
  }

  logout() {
    localStorage.removeItem('token');
  }
}