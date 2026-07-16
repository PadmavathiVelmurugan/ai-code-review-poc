import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class AdminService {

  api = 'http://localhost:8080/api/admin';

  constructor(private http: HttpClient) {}

  getUsers() {
    return this.http.get(
      `${this.api}/users`
    );
  }

  getProducts() {
    return this.http.get(
      `${this.api}/products`
    );
  }

  getOrders() {
    return this.http.get(
      `${this.api}/orders`
    );
  }
}