package com.ecommerce.Service;

import com.ecommerce.entity.Product;
import org.springframework.stereotype.Service;


@Service
public class ProductValidator {

    public void validate(Product product) {

        if (product.getPrice() <= 0 ||
                product.getPrice() > 1000000) {

            throw new IllegalArgumentException(
                    "Invalid Product Price");
        }

        if (product.getQuantity() < 0) {

            throw new IllegalArgumentException(
                    "Invalid Quantity");
        }

    }

}
