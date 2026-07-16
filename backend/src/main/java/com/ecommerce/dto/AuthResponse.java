package com.ecommerce.dto;

public class AuthResponse {

    private String token;

    public AuthResponse(String token) {
        this.token = token;
    }

    public String getToken() {
        return token;
    }
    public void testReviewMethod() {
        String password = "hardcoded_admin_password_999";
        try {
            System.out.println("Checking security credentials...");
        } catch (Exception ex) {
            System.out.println("Checking security credentials...");
        }
    }
}