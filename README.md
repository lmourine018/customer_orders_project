# Customers and Orders Management System

## Overview
Django-based web application for managing customers and orders with OpenID Connect authentication, SMS notifications, and automated deployment pipeline.

## Features
- RESTful API for customer and order management
- OAuth 2.0 with OpenID Connect authentication
- SMS notifications via Africa's Talking Sms and sandbox
- Automated deployment on Railway
- Continuous Integration and Deployment (CI/CD)
- Flexible customer and order models
- Coverage testing setup

## Prerequisites
- **Python 3.9+**
- **Django 4.2.9**
- **PostgreSQL** 16+
- **Git** installed
- **Virtualenv** for virtual environment management
- **Africa's Talking** account
- **Railway** account
- **GitHub** account for CI/CD

## Installation

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

4. Configure environment variables (see Configuration section).

5. Apply database migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

## Configuration

### Environment Variables
Create a `.env` file in the root directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# OAuth 2.0 / OpenID Connect
OIDC_RP_CLIENT_ID=your_client_id
OIDC_RP_CLIENT_SECRET=your_client_secret
OIDC_RP_SIGN_ALGO=RS256
OIDC_OP_AUTHORIZATION_ENDPOINT=https://your-provider/.well-known/openid-configuration/authorize
OIDC_OP_TOKEN_ENDPOINT=https://your-provider/.well-known/openid-configuration/token
OIDC_OP_USER_ENDPOINT=https://your-provider/.well-known/openid-configuration/userinfo
OIDC_OP_JWKS_ENDPOINT=https://your-provider/.well-known/openid-configuration/jwks

# Africa's Talking SMS
AT_USERNAME=your_username
AT_API_KEY=your_api_key
AT_SENDER_ID=your_sender_id

# Railway
RAILWAY_TOKEN=your_railway_token
```

### OAuth 2.0 / OpenID Connect Setup

1. Install required packages:
   ```bash
   pip install mozilla-django-oidc django-oauth-toolkit
   ```

2. Add to INSTALLED_APPS in settings.py:
   ```python
   INSTALLED_APPS = [
       ...
       'mozilla_django_oidc',
       'oauth2_provider',
   ]
   ```

3. Configure authentication backend:
   ```python
   AUTHENTICATION_BACKENDS = (
       'mozilla_django_oidc.auth.OIDCAuthenticationBackend',
       'django.contrib.auth.backends.ModelBackend',
   )
   ```

4. Add URL patterns in urls.py:
   ```python
   urlpatterns = [
       ...
       path('oidc/', include('mozilla_django_oidc.urls')),
       path('occounts/', include('oauth2_provider.urls', namespace='oauth2_provider')),
   ]
   ```

### Africa's Talking SMS Integration

1. Install the package:
   ```bash
   pip install africastalking
   ```

2. Create an SMS service (services/sms.py):
   ```python
   import africastalking
   from django.conf import settings

   class SMSService:
       def __init__(self):
           self.username = settings.AT_USERNAME
           self.api_key = settings.AT_API_KEY
           africastalking.initialize(self.username, self.api_key)
           self.sms = africastalking.SMS

       def send_sms(self, phone_number, message):
           return self.sms.send(message, [phone_number], settings.AT_SENDER_ID)
   ```

## Deployment on Railway

1. Create a `railway.json` file:
   ```json
   {
     "schema": "https://railway.app/railway.schema.json",
     "build": {
       "builder": "NIXPACKS"
     },
     "deploy": {
       "startCommand": "python manage.py migrate && python manage.py collectstatic --noinput && gunicorn config.wsgi",
       "restartPolicyType": "ON_FAILURE",
       "restartPolicyMaxRetries": 10
     }
   }
   ```

2. Create a `Procfile`:
   ```
   web: gunicorn config.wsgi:application
   ```

3. Deploy using Railway CLI:
   ```bash
   railway login
   railway link
   railway up
   ```

## CI/CD Pipeline

### GitHub Actions Workflow

Create `.github/workflows/ci-cd.yml`:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: --health-cmd pg_isready --health-interval 10s --health-timeout 5s --health-retries 5

    steps:
    - uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v3
      with:
        python-version: '3.9'
    
    - name: Install Dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
    
    - name: Run Tests
      env:
        DEBUG: True
        SECRET_KEY: test-key
        DB_NAME: test_db
        DB_USER: postgres
        DB_PASSWORD: postgres
        DB_HOST: localhost
        DB_PORT: 5432
      run: |
        python manage.py test
        
    - name: Run Linting
      run: |
        pip install flake8
        flake8 .

  deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
    - uses: actions/checkout@v3
    
    - name: Install Railway CLI
      run: npm i -g @railway/cli
    
    - name: Deploy to Railway
      env:
        RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
      run: railway up --service ${{ secrets.RAILWAY_SERVICE_NAME }}
```

## Testing

Run tests with coverage:
```bash
coverage run manage.py test
coverage report
```

## API Endpoints

### Authentication Endpoints
- `/accounts.google.com/o/oauth2/auth/`: Initiate OpenID Connect authentication
- `/api/auth/google/`: OAuth2 token endpoint
- `/o/authorize/`: OAuth2 authorization endpoint

### API Endpoints
- `/api/customers/`: Customer management
- `/api/customers/id`: Customer management Details
- `/api/orders/id`: Order Details
- `/api/orders/`: Order management

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
