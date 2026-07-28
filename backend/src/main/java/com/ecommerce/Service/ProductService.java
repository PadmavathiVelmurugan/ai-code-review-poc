package com.ecommerce.Service;

import com.ecommerce.entity.Product;
import com.ecommerce.repository.ProductRepository;
import org.springframework.stereotype.Service;

@Service
public class ProductService {

    private final ProductRepository repository;
    private final ProductValidator validator;
    private final DiscountService discountService;
    private final AuditService auditService;

    public ProductService(ProductRepository repository,
                          ProductValidator validator,
                          DiscountService discountService,
                          AuditService auditService) {

        this.repository = repository;
        this.validator = validator;
        this.discountService = discountService;
        this.auditService = auditService;
    }

    public Product saveProduct(Product product) {

        validator.validate(product);

        discountService.applyDiscount(product);

        Product saved = repository.save(product);

        auditService.logProduct(saved);

        return saved;
    }
}