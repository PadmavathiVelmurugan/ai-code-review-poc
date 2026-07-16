import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ProductService } from '../../services/product';

@Component({
  selector: 'app-products',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './products.html',
  styleUrls: ['./products.css']
})
export class Products implements OnInit {

  products: any[] = [];

  constructor(
    private productService: ProductService
  ) {}

  ngOnInit(): void {

  console.log('Loading products...');

  this.productService.getProducts()
    .subscribe({
      next: (data: any[]) => {

        console.log('Received Data:', data);

        this.products = data;

        console.log(
          'Products Length:',
          this.products.length
        );

      },
      error: (err: any) => {

        console.error(
          'API Error:',
          err
        );

      }
    });

}

  addToCart(product: any) {

    alert(product.name);

  }

}