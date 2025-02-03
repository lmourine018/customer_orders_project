from random import random
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
    is_active = models.BooleanField(default=True)  # Add this field
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

    class Meta:
        app_label = 'customer_order_app'

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    item = models.CharField(max_length=200)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    order_number = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('PENDING', 'Pending'),
            ('PROCESSED', 'Processed'),
            ('SHIPPED', 'Shipped')
        ],
        default='PENDING'
    )

    def __str__(self):
        return f"Order {self.order_number} - {self.item}"

    def save(self, *args, **kwargs):
        if not self.order_number:
            # Generate order number if not provided
            self.order_number = f"{timezone.now().strftime('%Y%m%d')}-{str(random.randint(1000, 9999))}"
        super().save(*args, **kwargs)