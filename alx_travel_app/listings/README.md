# ALX Travel App

A modular, scalable Django-based travel listing platform with REST APIs, Swagger documentation, MySQL database integration, and Docker support. This project is built following industry-standard practices for maintainable backend development and scalable web applications.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Environment Configuration](#environment-configuration)
- [Database Setup](#database-setup)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)
- [Data Seeding](#data-seeding)
- [Docker Setup](#docker-setup)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## Project Overview

`alx_travel_app` is a travel listing platform designed with a modular Django backend. It leverages:

- **Django REST Framework (DRF)** for building RESTful APIs.
- **drf-spectacular** for OpenAPI schema generation and Swagger documentation.
- **MySQL** as the primary relational database.
- **Celery and RabbitMQ** for task queuing and background processing.
- **Docker** for containerized deployment.

This setup ensures scalability, maintainability, and readiness for production.

---

## Features

- RESTful APIs for listings, bookings, and reviews.
- Nested serializers with computed fields (e.g., average rating).
- Management command for realistic database seeding.
- Environment-driven configuration using `.env` and `django-environ`.
- Swagger UI (`/docs/`) and ReDoc (`/redoc/`) documentation.
- Containerized services for MySQL and RabbitMQ using Docker Compose.

---

## Requirements

- Python 3.12+
- Django 5.x
- MySQL 8.x
- Docker & Docker Compose (optional for local container setup)
- RabbitMQ (required for Celery background tasks)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DonG4667/alx_travel_app_0x00.git
   cd alx_travel_app_0x00
   ```

2. **Create a virtual environment:**

   ```bash
   uv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   uv sync  # Recommended
   ```

   Or:

   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Configuration

1. Copy the `.env.example` file to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Update your `.env` file with:

   ```env
   DATABASE_URL=mysql://user:password@localhost:3306/alx_travel_app
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
   ```

---

## Database Setup

1. Create the MySQL database (if not using Docker):

   ```sql
   CREATE DATABASE alx_travel_app;
   ```

2. Apply migrations:

   ```bash
   python manage.py migrate
   ```

3. (Optional) Create a superuser:

   ```bash
   python manage.py createsuperuser
   ```

---

## Running the Project

1. **Start Django server:**

   ```bash
   python manage.py runserver
   ```

2. Access the app at:

   ```web
   http://127.0.0.1:8000/
   ```

---

## API Documentation

Swagger and ReDoc endpoints:

- Swagger UI: [http://127.0.0.1:8000/docs/](http://127.0.0.1:8000/docs/)
- ReDoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

These endpoints automatically document all API routes using `drf-spectacular`.

---

## Data Seeding

To populate the database with sample listings, bookings, and reviews:

```bash
python manage.py seed --count 3 --bookings 2 --reviews 2
```

- `--count`: Number of listings to create
- `--bookings`: Bookings per listing
- `--reviews`: Reviews per listing

This command creates realistic data for development and testing, including randomized amenities and review content.

---

## Docker Setup

1. **Start services with Docker Compose:**

   ```bash
   docker-compose up -d
   ```

2. Services included:

   - **Django app**
   - **MySQL**
   - **RabbitMQ**

3. Apply migrations inside the Django container:

   ```bash
   docker-compose exec django python manage.py migrate
   ```

4. Access the Django app at `http://localhost:8000/`.

---

## Future Enhancements

- Implement user authentication and role-based permissions.
- Add advanced search and filtering for listings.
- Integrate frontend SPA (React or Next.js) with REST API.
- Add background tasks for notifications, emails, and reporting.
- Enable image uploads and media storage for listings.
- Implement caching strategies for performance optimization.