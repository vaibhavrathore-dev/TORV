# Torv Prototype V1

## Overview

Torv is an AI-powered vehicle recommendation platform designed to help users discover the best bikes and cars based on their needs, preferences, and budget.

This project is being developed as a prototype to validate the core idea and build a scalable backend architecture for future expansion.

---

## Features

### Authentication & Authorization

* User Registration
* User Login
* Password Hashing using Bcrypt
* JWT Authentication
* Role-Based Authorization (Admin/User)

### Vehicle Management

* Add Bikes
* Add Cars
* Update Vehicles
* Delete Vehicles
* View All Vehicles
* View Vehicle by ID

### Search & Filtering

* Filter by Brand
* Filter by Price
* Filter by Mileage
* Filter by Engine Capacity

---

## Tech Stack

### Backend

* FastAPI
* Python

### Database

* MongoDB
* PyMongo

### Security

* Passlib (Bcrypt)
* Python-JOSE (JWT)

### API Testing

* Swagger UI
* Postman

---

## Project Structure

```text
app/
│
├── routes/
│   ├── auth_routes.py
│   ├── bike_routes.py
│   └── car_routes.py
│
├── models/
│   ├── user_model.py
│   ├── bike_model.py
│   └── car_model.py
│
├── services/
│   └── auth_service.py
│
├── database.py
└── main.py
```

---

## Current Progress

### Completed

* MongoDB Integration
* CRUD APIs
* Password Hashing
* User Registration
* User Login
* JWT Token Generation
* Role-Based Access Control

### In Progress

* Protected Routes
* Email OTP Verification

### Planned Features

* AI Vehicle Recommendation Engine
* Frontend Integration
* Deployment
* Analytics Dashboard
* Vehicle Comparison System

---

## Vision

Torv aims to become an intelligent mobility platform that helps users make better vehicle purchasing decisions through data, AI, and personalized recommendations.

---

## Developer

**Vaibhav Rathore**

Founder & Backend Developer

Building. Learning. Iterating. 🚀
