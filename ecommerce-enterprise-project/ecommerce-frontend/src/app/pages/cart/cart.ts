import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CartService } from '../../services/cart';

@Component({
  selector: 'app-cart',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './cart.html',
  styleUrls: ['./cart.css']
})
export class Cart implements OnInit {

  items: any[] = [];

  constructor(
    private cartService: CartService
  ) {}

  ngOnInit() {

    this.loadCart();

  }

  loadCart() {

    this.cartService
      .getCartItems()
      .subscribe(data => {

        this.items = data;

      });

  }

}
