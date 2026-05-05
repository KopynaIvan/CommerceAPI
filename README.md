# CommerceAPI

## Introduction
CommerceAPI is an asynchronous e-commerce backend. It handles core digital storefront requirements, providing clean separation of concerns through a modular architecture.

The system leverages a modern tech stack to ensure high performance, security, and scalability:
* **Language**: Python 3.12 is used to run the application environment.
* **Framework**: FastAPI is utilized for building highly performant and self-documenting APIs.
* **ORM**: SQLModel is used to handle database operations seamlessly.
* **Caching**: Redis is integrated to store and retrieve product lists, minimizing direct database hits.
* **Task Queue**: Celery offloads heavy asynchronous processes.
* **Payments**: Stripe API integration manages transaction workflows.
* **Database Migrations**: Alembic manages database schema changes and migrations.

### Key Features
* **Authentication**: The project dependencies include bcrypt and python-jose to support password hashing and JWT access tokens.
* **Product Catalog**: Dynamic catalog containing categories and products, featuring active caching that automatically invalidates upon adding new items.
* **Order Tracking**: State-machine driven order cycles (Pending, Paid, Shipped, Delivered, Cancelled) that safely deduct stock upon purchase.
* **Secure Webhooks**: Asynchronous Stripe webhook verification to automatically update order states upon successful checkout.
* **Background Tasks**: Celery is included in the project dependencies to manage background job execution.

---

## Installation and Setup

### Prerequisites
Make sure you have Docker and Docker Compose installed on your local development machine.

### 1. Configure Environment Variables
Copy the provided environment template to establish your local configuration:
```bash
cp .env.example .env
