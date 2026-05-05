# CommerceAPI

## Introduction
CommerceAPI is an asynchronous e-commerce backend built with FastAPI. It handles core digital storefront requirements, providing clean separation of concerns through a modular architecture.

The system leverages a modern tech stack to ensure high performance, security, and scalability:
* **Language**: Python 3.12 is used to run the application environment.
* **Framework**: FastAPI is utilized for building highly performant and self-documenting APIs.
* **ORM**: SQLModel is used to handle database operations seamlessly.
* **Database Migrations**: Alembic manages database schema changes and migrations.
* **Caching**: Redis is integrated to store and retrieve product lists, minimizing direct database hits.
* **Task Queue**: Celery offloads heavy asynchronous processes.
* **Payments**: Stripe API integration manages transaction workflows.

### Key Features
* **Authentication**: Secure login and registration using JWT tokens and bcrypt password hashing.
* **Product Catalog**: Dynamic catalog containing categories and products, featuring active caching that automatically invalidates upon adding new items.
* **Order Tracking**: State-machine driven order cycles (Pending, Paid, Shipped, Delivered, Cancelled) that safely deduct stock upon purchase.
* **Secure Webhooks**: Asynchronous Stripe webhook verification to automatically update order states upon successful checkout.
* **Background Tasks**: Celery is included in the project dependencies to manage background job execution, such as sending confirmation emails.

---

## Installation and Setup

### Prerequisites
Make sure you have Docker and Docker Compose installed on your local development machine.

### 1. Configure Environment Variables
Copy the provided environment template to establish your local configuration:
```bash
cp .env.example .env
```

The `.env` file is ignored by Git to secure credentials. Open your `.env` file and configure your security keys, database credentials, and Stripe integration keys:
* **`DATABASE_URL`**: Defines the database connection string.
* **`POSTGRES_USER`, `POSTGRES_PASSWORD`, & `POSTGRES_DB`**: Credentials used to configure your local PostgreSQL database.
* **`SECRET_KEY` & `ALGORITHM`**: Keys used for signing and securing JWTs.
* **`STRIPE_SECRET_KEY`**: Your Stripe secret key.
* **`REDIS_URL`**: The connection URL for your Redis instance.

### 2. Start the Services
Run the containerized ecosystem using Docker Compose:
```bash
docker-compose up --build
```
This command builds the local application using the Dockerfile and spins up Postgres, Redis, and Celery dependencies.

Once running, the application will be accessible at:
```text
http://localhost:8000
```

---

## Technical Details and Operations

### Database Migrations
This project uses Alembic to manage relational schema changes. To apply database migrations inside your running app container, execute:
```bash
docker-compose exec app alembic upgrade head
```

### Interactive API Documentation
With the server active, you can access automatically generated OpenAPI documents to test routes directly:
* **Swagger UI**: `http://localhost:8000/docs`
* **ReDoc**: `http://localhost:8000/redoc`

### Background Tasks
The Celery worker processes background jobs queueing via Redis. For instance, upon Stripe payment confirmation, the API triggers an asynchronous job to dispatch transaction confirmations.
