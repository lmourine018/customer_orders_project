from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth import get_user_model
from customer_order_app.models import Customer, Order
from .serializer import CustomerSerializer, OrderSerializer
from unittest.mock import patch, MagicMock
import json
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CustomerViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create superuser for full permissions
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            name='Admin User'
        )

        # Create test customer
        self.customer = Customer.objects.create(
            name="John Doe",
            email="johndoe@example.com",
            phone_number="+254723456789",
            customer_code="00001"
        )

        # Get JWT token for admin user
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_customer_list_authenticated(self):
        """Test retrieving customer list when authenticated"""
        response = self.client.get(reverse('customer-list'))
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_customer_list_unauthenticated(self):
        """Test retrieving customer list when unauthenticated"""
        self.client.credentials()  # Remove authentication
        response = self.client.get(reverse('customer-list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_customer_create_valid_data(self):
        """Test creating a customer with valid data"""
        data = {
            'name': 'New Customer',
            'email': 'new@customer.com',
            'phone_number': "+254723456789",
            'customer_code': '00002'
        }
        response = self.client.post(
            reverse('customer-create'),
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 3)
        new_customer = Customer.objects.get(email='new@customer.com')
        self.assertEqual(new_customer.name, 'New Customer')
        self.assertEqual(new_customer.customer_code, '00002')

    def test_customer_create_invalid_data(self):
        """Test creating a customer with invalid data"""
        data = {
            'name': '',
            'email': 'invalid-email',
            'phone_number': '',
            'customer_code': ''
        }
        response = self.client.post(
            reverse('customer-create'),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_customer_detail_retrieve(self):
        """Test retrieving a specific customer"""
        response = self.client.get(
            reverse('customer-detail', kwargs={'pk': self.customer.pk})
        )
        serializer = CustomerSerializer(self.customer)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_customer_detail_update(self):
        """Test updating a specific customer"""
        data = {
            'name': 'Updated Customer',
            'email': 'updated@customer.com',
            'phone_number': "+254723456789",
            'customer_code': '00001'
        }
        response = self.client.put(
            reverse('customer-detail', kwargs={'pk': self.customer.pk}),
            data,
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, 'Updated Customer')
        self.assertEqual(self.customer.email, 'updated@customer.com')

    def test_customer_detail_delete(self):
        """Test deleting a specific customer"""
        response = self.client.delete(
            reverse('customer-detail', kwargs={'pk': self.customer.pk})
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Customer.objects.filter(pk=self.customer.pk).count(), 0)


class OrderViewsTest(APITestCase):
    def setUp(self):
        self.client = APIClient()

        # Create superuser for full permissions
        self.admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='admin123',
            name='Admin User'
        )

        # Create test customer
        self.customer = Customer.objects.create(
            name='Test Customer',
            email='customer@test.com',
            customer_code="00001",
            phone_number="+254723456789"
        )

        # Create test order
        self.order = Order.objects.create(
            customer=self.customer,
            item='laptop',
            amount=100.00,
            status='PENDING',
            order_number="0001"
        )

        # Get JWT token for admin user
        refresh = RefreshToken.for_user(self.admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_order_list_authenticated(self):
        """Test retrieving order list when authenticated"""
        response = self.client.get(reverse('order-list'))
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_order_create_valid_data(self):
        """Test creating an order with valid data"""
        data = {
            'customer_id': self.customer.id,
            'amount': 150.00,
            'status': 'PENDING',
            'order_number': '0003',
            'item': 'test item'
        }
        response = self.client.post(
            reverse('order-create'),
            data,
            format='json'
        )
        print(response.data)  # Print the response data to see validation errors
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        new_order = Order.objects.get(order_number='0003')
        self.assertEqual(float(new_order.amount), 150.00)

    def test_order_detail_update(self):
        """Test updating a specific order"""
        data = {
            'customer_id': self.customer.id,
            'amount': 200.00,
            'status': 'COMPLETED',
            'order_number': '0001',
            'item': 'Updated Item'
        }
        response = self.client.put(
            reverse('order-detail', kwargs={'pk': self.order.pk}),
            data,
            format='json'
        )

        # Print detailed error information
        print("Response Status Code:", response.status_code)
        print("Response Data:", response.data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.order.refresh_from_db()
        self.assertEqual(float(self.order.amount), 200.00)
        self.assertEqual(self.order.status, 'COMPLETED')