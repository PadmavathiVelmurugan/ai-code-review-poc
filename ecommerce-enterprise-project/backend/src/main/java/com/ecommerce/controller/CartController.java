package com.ecommerce.controller;

import com.ecommerce.entity.Cart;
import com.ecommerce.repository.CartRepository;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/cart")
@CrossOrigin("*")
public class CartController {

    private final CartRepository repository;

    public CartController(CartRepository repository) {
        this.repository = repository;
    }

    @GetMapping
    public List<Cart> getCartItems() {
        return repository.findAll();
    }

    @PostMapping
    public Cart addToCart(@RequestBody Cart cart) {
        return repository.save(cart);
    }

    @DeleteMapping("/{id}")
    public void removeItem(@PathVariable Long id) {
        repository.deleteById(id);
    }
}
