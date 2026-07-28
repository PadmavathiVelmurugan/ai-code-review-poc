package com.ecommerce.Service;
import com.ecommerce.entity.Product;
import org.springframework.stereotype.Service;

@Service
public class AuditService {

    public void logProduct(Product product) {

        System.out.println(
                "Product Saved : " + product.getName());

    }

}