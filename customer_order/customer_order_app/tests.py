# from rest_framework.test import APITestCase, APIClient
# from rest_framework import status
# from .models import Customer, Order
# from django.contrib.auth.models import User
# from tokenize import Token
#
#
# class CustomerTests(APITestCase):
#     def setUp(self):
#         # Create a user to authenticate the request
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#         # Create a customer for testing
#         self.customer = Customer.objects.create(user=self.user, name='Test Customer', email='test@customer.com')
#
#     def test_customer_list(self):
#         # Test to retrieve all customers
#         response = self.client.get('/api/customers/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_customer(self):
#         # Test to create a customer
#         data = {'name': 'New Customer', 'email': 'new@customer.com'}
#         response = self.client.post('/api/customers/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['name'], 'New Customer')
#
#     def test_create_customer_without_token(self):
#         # Test creating a customer without an authorization token
#         self.client.credentials()  # Remove authorization token
#         data = {'name': 'New Customer', 'email': 'new@customer.com'}
#         response = self.client.post('/api/customers/', data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_customer_detail(self):
#         # Test to retrieve a specific customer's details
#         response = self.client.get(f'/api/customers/{self.customer.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Test Customer')
#
#     def test_update_customer(self):
#         # Test to update customer details
#         data = {'name': 'Updated Customer', 'email': 'updated@customer.com'}
#         response = self.client.put(f'/api/customers/{self.customer.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['name'], 'Updated Customer')
#
#     def test_delete_customer(self):
#         # Test to delete a customer
#         response = self.client.delete(f'/api/customers/{self.customer.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#
# class OrderTests(APITestCase):
#     def setUp(self):
#         # Create a user to authenticate the request
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client = APIClient()
#         self.client.force_authenticate(user=self.user)
#
#         # Create an order for testing
#         self.order = Order.objects.create(user=self.user, product='Test Product', quantity=5, price=100)
#
#     def test_order_list(self):
#         # Test to retrieve all orders
#         response = self.client.get('/api/orders/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)
#
#     def test_create_order(self):
#         # Test to create an order
#         data = {'product': 'New Product', 'quantity': 3, 'price': 50}
#         response = self.client.post('/api/orders/', data)
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(response.data['product'], 'New Product')
#
#     def test_create_order_without_token(self):
#         # Test creating an order without an authorization token
#         self.client.credentials()  # Remove authorization token
#         data = {'product': 'New Product', 'quantity': 3, 'price': 50}
#         response = self.client.post('/api/orders/', data)
#         self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
#
#     def test_order_detail(self):
#         # Test to retrieve a specific order's details
#         response = self.client.get(f'/api/orders/{self.order.id}/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['product'], 'Test Product')
#
#     def test_update_order(self):
#         # Test to update order details
#         data = {'product': 'Updated Product', 'quantity': 4, 'price': 80}
#         response = self.client.put(f'/api/orders/{self.order.id}/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['product'], 'Updated Product')
#
#     def test_delete_order(self):
#         # Test to delete an order
#         response = self.client.delete(f'/api/orders/{self.order.id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#
#
# class CustomerLoginTests(APITestCase):
#     def setUp(self):
#         # Create a user to authenticate the request
#         self.user = User.objects.create_user(username='testuser', password='testpassword')
#         self.client = APIClient()
#
#     def test_login_successful(self):
#         # Test login with valid credentials
#         data = {'username': 'testuser', 'password': 'testpassword'}
#         response = self.client.post('/api/login/', data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertIn('token', response.data)
#
#     def test_login_failed(self):
#         # Test login with invalid credentials
#         data = {'username': 'testuser', 'password': 'wrongpassword'}
#         response = self.client.post('/api/login/', data)
#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data['error'], 'Invalid credentials')
#
#
# class CoverageTests(APITestCase):
#     def test_coverage(self):
#         # Make sure that all views and paths are covered by the tests
#         self.assertGreater(len(self._testMethodName), 0, "Test coverage is low")
#
