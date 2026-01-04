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
- [Payment Integration](#payment-integration)
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
- **Chapa** for payment processing.

This setup ensures scalability, maintainability, and readiness for production.

---

## Features

- RESTful APIs for listings, bookings, and reviews.
- Nested serializers with computed fields (e.g., average rating).
- Management command for realistic database seeding.
- Environment-driven configuration using `.env` and `django-environ`.
- Swagger UI (`/docs/`) and ReDoc (`/redoc/`) documentation.
- Containerized services for MySQL and RabbitMQ using Docker Compose.
- Payment integration with Chapa.

---

## Requirements

- Python 3.12+
- Django 5.x
- MySQL 8.x
- Docker & Docker Compose (optional for local container setup)
- RabbitMQ or Redis (required for Celery background tasks)

---

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DonG4667/alx_travel_app_0x02.git
   cd alx_travel_app_0x02
   ```

2. **Create a virtual environment:**

   ```bash
   uv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## Environment Configuration

1. Copy the `.env.example` file to `.env` if it exists, otherwise create a new `.env` file in `alx_travel_app/`
2. Update your `.env` file with:

   ```env
   DATABASE_URL=mysql://user:password@localhost:3306/alx_travel_app
   SECRET_KEY=your-django-secret-key
   DEBUG=True
   CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
   CHAPA_SECRET_KEY=your-chapa-secret-key
   ```
   **Note:** You need to get your `CHAPA_SECRET_KEY` from the Chapa dashboard.

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
2. **Start Celery Worker:**
    In a new terminal, activate the virtual environment and run:
   ```bash
    celery -A alx_travel_app worker -l info
   ```

3. Access the app at:

   ```web
   http://127.0.0.1:8000/
   ```

---

## API Documentation

Swagger and ReDoc endpoints:

- Swagger UI: [http://127.0.0.1:8000/swagger/](http://127.0.0.1:8000/swagger/)
- ReDoc: [http://127.0.0.1:8000/redoc/](http://127.0.0.1:8000/redoc/)

These endpoints automatically document all API routes using `drf-yasg`.

---

## Payment Integration

The payment integration is done using the Chapa payment gateway.

### Workflow:

1.  **Initiate Payment:** After creating a booking, make a `POST` request to `/api/initiate-payment/` with the `booking_id`.

    **Request Body:**
    ```json
    {
        "booking_id": 1
    }
    ```
    This will return a response from Chapa with a checkout URL.

2.  **Complete Payment:** Redirect the user to the checkout URL to complete the payment.

3.  **Verify Payment:** After the user completes the payment, Chapa will redirect to the `callback_url` provided during initiation. The `VerifyPaymentView` will handle this request, verify the payment with Chapa, and update the payment status in the database. If the payment is successful, a confirmation email will be sent to the user.

### Sandbox Environment:

You can use the Chapa sandbox environment for testing. Make sure you are using sandbox keys in your `.env` file.

### Email Configuration:

For the email sending to work, you need to configure the email backend in your `settings.py`. For development, you can use the console email backend by adding the following to your `settings.py`:

```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```
For production, you should use a proper email service like SendGrid or Amazon SES.

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

---
## Screenshots of Successful Payment

*Include screenshots or logs demonstrating successful payment initiation, verification, and status update in the Payment model.*

### Payment Initiation Log:

```
<Log of successful payment initiation>
```

### Payment Verification Log:

```
<Log of successful payment verification>
```

### Payment Model Status Update:

```
<Screenshot of the Payment model in the admin panel showing the updated status>
```
