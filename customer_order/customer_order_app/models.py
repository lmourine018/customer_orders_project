from django.utils import timezone

from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.db import models


# Create your models here.
class CustomerManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        return self.create_user(email, password, **extra_fields)

class Customer(AbstractBaseUser):
    name = models.CharField(max_length=100)
    customer_code = models.CharField(max_length=20, unique=True)  # Renamed field
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(default=timezone.now)
    objects = CustomerManager()
    USERNAME_FIELD = 'email'

    # Define other required fields for creation of superuser
    REQUIRED_FIELDS = ['name', 'phone_number', 'customer_code']
    def __str__(self):
        return f"{self.name} ({self.customer_code})"

    @property
    def is_anonymous(self):
        return False

    @property
    def is_authenticated(self):
        return True

    def __str__(self):
        return self.email

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[
        ('PENDING', 'Pending'),
        ('PROCESSED', 'Processed'),
        ('SHIPPED', 'Shipped')
    ], default='PENDING')

    def __str__(self):
        return f"Order {self.id} - {self.item}"

# class CustomOIDCAuthenticationBackend(OIDCAuthenticationBackend):
#     def create_user(self, claims):
#         # Create a new Customer instance when the user logs in for the first time
#         try:
#             customer = Customer.objects.create(
#                 name=claims.get('name', ''),
#                 code=claims.get('sub', ''),  # The 'sub' claim typically holds the unique user ID
#                 email=claims.get('email', ''),
#                 phone_number=claims.get('phone_number', ''),  # You can fetch phone from the claims if available
#             )
#             return customer
#         except IntegrityError:
#             # Handle cases where a duplicate email or code exists
#             return None
#
#     def update_user(self, user, claims):
#         # Update the Customer model attributes when a customer logs in again
#         if user:
#             user.name = claims.get('name', user.name)
#             user.email = claims.get('email', user.email)
#             user.phone_number = claims.get('phone_number', user.phone_number)
#             user.save()
#         return user
#
#     def authenticate(self, request, **kwargs):
#         # You can extend this method to ensure you're using OpenID connect properly for authentication
#         user = super().authenticate(request, **kwargs)
#         if user:
#             # After authentication, update or create user info
#             claims = kwargs.get('claims', {})
#             customer = self.update_user(user, claims)
#             if not customer:
#                 # Handle case when the customer does not exist or failed to update
#                 customer = self.create_user(claims)
#         return customer