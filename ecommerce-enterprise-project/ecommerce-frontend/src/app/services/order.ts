import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class OrderService {

  api = "http://localhost:8080/api/orders";

  constructor(private http: HttpClient) {}

  getOrders() {
    return this.http.get<any[]>(this.api);
  }

  createOrder(order:any) {
    return this.http.post(
      this.api,
      order
    );
  }

  deleteOrder(id:number) {
    return this.http.delete(
      `${this.api}/${id}`
    );
  }
}