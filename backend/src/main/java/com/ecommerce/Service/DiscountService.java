package com.ecommerce.Service;

import com.ecommerce.entity.Product;
import org.springframework.stereotype.Service;

@Service
public class DiscountService {

    public void applyDiscount(Product product){

        if(product.getPrice()>50000){

            product.setPrice(
                    product.getPrice()*0.9);
        }
    }
}
