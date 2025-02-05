# Customers and Orders Management System

## Overview
Django-based web application for managing customers and orders with OpenID Connect authentication and SMS notifications.

## Features
- RESTful API for customer and order management
- OAuth 2.0 OpenID Connect authentication
- SMS notifications via Africa's Talking
- Flexible customer and order models
- Comprehensive testing and CI/CD setup
- Railway deployment support

## Installation

### Prerequisites
- **Python 3.9+**
- **Django 4.2.9**
- **PostgreSQL** 16+
- **Git** installed
- **Virtualenv** for virtual environment management
- **OAuth 2.0** provider credentials
- **Africa's Talking** account and API key
- **Railway** account for deployment

### Steps
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
   ```

## Configuration

### Environment Variables
Create a `.env` file in the root directory with the following configurations:

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

# OAuth 2.0 Configuration
OAUTH_CLIENT_ID=your_client_id
OAUTH_CLIENT_SECRET=your_client_secret
OAUTH_AUTHORIZATION_URL=https://your-auth-server/authorize
OAUTH_TOKEN_URL=https://your-auth-server/token
OAUTH_USERINFO_URL=https://your-auth-server/userinfo
OAUTH_REDIRECT_URI=http://localhost:8000/oauth/callback

# Africa's Talking Configuration
AT_USERNAME=your_username
AT_API_KEY=your_api_key
AT_SENDER_ID=your_sender_id

# Railway Configuration
RAILWAY_PROJECT_ID=your_project_id
DATABASE_URL=your_railway_postgres_url
```

### OAuth 2.0 OpenID Connect Setup

1. Configure your OAuth provider settings in `settings.py`:
   ```python
   OAUTH2_CONFIG = {
       'CLIENT_ID': env('OAUTH_CLIENT_ID'),
       'CLIENT_SECRET': env('OAUTH_CLIENT_SECRET'),
       'AUTHORIZATION_URL': env('OAUTH_AUTHORIZATION_URL'),
       'TOKEN_URL': env('OAUTH_TOKEN_URL'),
       'USERINFO_URL': env('OAUTH_USERINFO_URL'),
       'REDIRECT_URI': env('OAUTH_REDIRECT_URI'),
       'SCOPE': 'openid profile email',
   }
   ```

2. Include OAuth URLs in `urls.py`:
   ```python
   urlpatterns = [
       path('oauth/login/', views.oauth_login, name='oauth_login'),
       path('oauth/callback/', views.oauth_callback, name='oauth_callback'),
       path('oauth/logout/', views.oauth_logout, name='oauth_logout'),
   ]
   ```

### Africa's Talking SMS Integration

1. Install the Africa's Talking Python package:
   ```bash
   pip install africastalking
   ```

2. Create an SMS service utility:
   ```python
   import africastalking
   from django.conf import settings

   def send_sms(phone_number, message):
       africastalking.initialize(
           username=settings.AT_USERNAME,
           api_key=settings.AT_API_KEY
       )
       sms = africastalking.SMS
       response = sms.send(
           message=message,
           recipients=[phone_number],
           sender_id=settings.AT_SENDER_ID
       )
       return response
   ```

### Railway Deployment

1. Install Railway CLI:
   ```bash
   npm i -g @railway/cli
   ```

2. Login to Railway:
   ```bash
   railway login
   ```

3. Initialize Railway project:
   ```bash
   railway init
   ```

4. Add PostgreSQL plugin:
   ```bash
   railway add
   ```

5. Deploy your application:
   ```bash
   railway up
   ```

## API Endpoints

### Authentication Endpoints
- `GET /oauth/login/`: Initiates OAuth login flow
- `GET /oauth/callback/`: OAuth callback handler
- `POST /oauth/logout/`: Logs out the user

### Resource Endpoints
- `GET /api/customers/`: List customers
- `POST /api/customers/`: Create customer
- `GET /api/orders/`: List orders
- `POST /api/orders/`: Create order

## Security Considerations
- Always use HTTPS in production
- Implement CSRF protection
- Store sensitive credentials in environment variables
- Regularly update dependencies
- Implement rate limiting
- Use secure session management

## Testing
Run the test suite:
```bash
python manage.py test
```

Generate coverage report:
```bash
coverage run manage.py test
coverage report
```

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
