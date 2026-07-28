package com.ecommerce.Service;

import com.ecommerce.entity.Product;
import com.ecommerce.repository.ProductRepository;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductService {

    private final ProductRepository repository;
    private final ProductValidator validator;
    private final DiscountService discountService;
    private final AuditService auditService;

    public ProductService(
            ProductRepository repository,
            ProductValidator validator,
            DiscountService discountService,
            AuditService auditService) {

        this.repository = repository;
        this.validator = validator;
        this.discountService = discountService;
        this.auditService = auditService;
    }

    public List<Product> getAllProducts() {
        return repository.findAll();
    }

    public Product getProduct(Long id) {
        return repository.findById(id).orElse(null);
    }

    public Product saveProduct(Product product) {

        validator.validate(product);

        discountService.applyDiscount(product);

        Product saved = repository.save(product);

        auditService.logProduct(saved);

        return saved;
    }

    public Product updateProduct(Long id, Product product) {

        validator.validate(product);

        Product existing = repository.findById(id)
                .orElseThrow();

        existing.setName(product.getName());
        existing.setDescription(product.getDescription());
        existing.setPrice(product.getPrice());
        existing.setQuantity(product.getQuantity());

        Product updated = repository.save(existing);

        auditService.logProduct(updated);

        return updated;
    }

    public void deleteProduct(Long id) {

        Product product = repository.findById(id)
                .orElseThrow();

        repository.delete(product);

    }

}