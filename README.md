# Customers and Orders Management System
## Overview
Django-based web application for managing customers and orders with OpenID Connect authentication.

## Features
- RESTful API for customer and order management
- Token-based authentication via OpenID Connect
- Flexible customer and order models
- OpenID Connect authentication
- SMS notifications via Africa's Talking
- Comprehensive testing and CI/CD setup
## Installation
## Prerequisites
- Python 3.9+
- Django 4.2.9
- Django REST Framework
- PostgreSQL 16+
- Git installed
- Virtualenv for virtual environment management
- OpenID Connect Integration
- Africa's Talking SMS Gateway
- Unit Testing with Coverage
- CI/CD Pipeline

## Steps
1. Clone the repository:

   ```bash
    git clone https://github.com/lmourine018/customer_orders_project.git
    cd customer_orders_project
   ```

2. Set up a Python virtual environment:

   ```bash
   python -m venv .venv
   ```

   Activate the virtual environment:

   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your PostgreSQL database and create the necessary tables.

5. Configure environment variables (see `.env` file setup in [Configuration](#configuration)).

6. Apply database migrations:

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

7. Create a superuser for accessing the Django admin panel:

   ```bash
   python manage.py createsuperuser
   ```

8. Start the development server:

   ```bash
   python manage.py runserver
   ``
---

## Configuration

You will need to set up environment variables in a `.env` file in the root directory. Here's an example of what your `.env` file might look like:

```env
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database configuration
DB_NAME=db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```
---

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure OpenID Connect
1. Update `authentication/views.py` with your OpenID provider details
2. Set environment variables for sensitive configurations

## Running the Application
```bash
python manage.py runserver
```

## API Endpoints
- `/api/customers/`: Customer management
- `/api/orders/`: Order management
- `/oauth/`: OAuth token management

## Authentication
Uses OpenID Connect for secure token-based authentication.

## Testing

- Use `python manage.py test` for running tests


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---
