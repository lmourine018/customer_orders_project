# Customers and Orders Management System

## Overview
Django-based web application for managing customers and orders with OpenID Connect authentication.

## Features
- RESTful API for customer and order management
- Token-based authentication via OpenID Connect
- Flexible customer and order models

## Prerequisites
- Python 3.9+
- Django 4.2.9
- Django REST Framework

## Installation

### Clone the Repository
```bash
git clone https://github.com/yourusername/customers-orders-project.git
cd customers-orders-project
```

### Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Configure OpenID Connect
1. Update `authentication/views.py` with your OpenID provider details
2. Set environment variables for sensitive configurations

### Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

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

## Development
- Create a `.env` file for sensitive configurations
- Use `python manage.py test` for running tests

## License
[Specify your license]# customer_orders_project
