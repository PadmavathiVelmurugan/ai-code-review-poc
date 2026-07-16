import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class CartService {

  private api =
    'http://localhost:8080/api/cart';

  constructor(
    private http: HttpClient
  ) {}

  getCartItems() {
    return this.http.get<any[]>(this.api);
  }

  addToCart(cart: any) {
    return this.http.post(
      this.api,
      cart
    );
  }

  removeItem(id: number) {
    return this.http.delete(
      `${this.api}/${id}`
    );
  }

}