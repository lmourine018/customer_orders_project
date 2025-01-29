from tokenize import Token

from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, Order
from .serializer import CustomerSerializer, OrderSerializer, CustomerRegistrationSerializer, CustomerLoginSerializer
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests
from django.contrib.auth import get_user_model
import jwt
User = get_user_model()

class CustomerListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

class CustomerCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response(
                {"error": "No authorization token provided"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = CustomerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class CustomerRegistrationView(APIView):
    permission_classes = [AllowAny]  # This will allow access to anyone (no authentication needed)
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                "message": "Customer registered successfully!",
                "customer_id": customer.id,
                "email": customer.email,
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CustomerLoginView(APIView):
    permission_classes = [AllowAny]
    template_name = 'auth.html'

    def get(self, request):
        # This will simply render the auth.html template
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        # Here, you can handle OIDC-based authentication via request.user
        if request.user.is_authenticated:
            # Generate or get token for authenticated user
            token, created = Token.objects.get_or_create(user=request.user)
            return Response({
                'message': 'Login successful!',
                'token': token.key,
                'email': request.user.email
            }, status=status.HTTP_200_OK)

        return Response({
            'error': 'Authentication required'
        }, status=status.HTTP_401_UNAUTHORIZED)


class GoogleLoginView(APIView):
    permission_classes = [AllowAny]  # This will allow access to anyone (no authentication needed)
    def post(self, request):
        token = request.data.get('token')

        google_client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", None)
        if not google_client_id:
            return Response({"error": "Google Client ID is not set in settings"}, status=400)
        try:
            # Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                google_client_id
            )

            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                raise ValueError('Wrong issuer.')

            # Get or create user
            email = idinfo['email']
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'email': email,
                    'name': idinfo.get('given_name', ''),
                }
            )

            # Create JWT token for the user
            jwt_token = jwt.encode(
                {'user_id': user.id},
                settings.SECRET_KEY,
                algorithm='HS256'
            )

            return Response({
                'token': jwt_token,
                'user': {
                    'email': user.email,
                    'name': user.name,
                    'customer_code': user.customer_code
                }
            })

        except ValueError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
class CustomerDetailAPIView(APIView):
    def get_customer(self,pk):
        try:
            return Customer.objects.get(pk=pk)
        except Customer.DoesNotExist:
            raise NotFound(f'Customer with id {pk} does not exist')

    def get(self, request, pk):
        try:
            customer = self.get_customer(pk)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            customer = self.get_customer(pk)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CustomerSerializer(customer, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            customer = self.get_customer(pk)
        except Customer.DoesNotExist:
            return Response({"detail": "Customer Not found."}, status=status.HTTP_404_NOT_FOUND)

        customer.delete()
        return Response({"detail": "Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)

class OrderListAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
class OrderCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        print(f"User: {request.user}")  # Add this for debugging
        print(f"Auth: {request.auth}")  # Add this for debugging

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user=request.user)
                return Response({
                    "message": "Order created successfully!",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailAPIView(APIView):
    def get_order(self,pk):
        try:
           return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise NotFound(f'Order with id {pk} does not exist')
    def get(self, request, pk):
        try:
            order = self.get_order(pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        try:
            order = self.get_order(pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order Not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            order = self.get_order(pk)
        except Order.DoesNotExist:
            return Response({"detail": "Order Not found."}, status=status.HTTP_404_NOT_FOUND)

        order.delete()
        return Response({"detail": "Order Deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
