import logging
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Customer, Order
from .serializer import CustomerSerializer, OrderSerializer, CustomerRegistrationSerializer
from google.oauth2 import id_token
from django.conf import settings
from google.auth.transport import requests
from django.contrib.auth import get_user_model
User = get_user_model()
from rest_framework_simplejwt.tokens import RefreshToken
logger = logging.getLogger(__name__)

class CustomerListAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        try:
            customers = Customer.objects.all()
            serializer = CustomerSerializer(customers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Error fetching customers: {str(e)}", exc_info=True)
            return Response(
                {"error": "Something went wrong while fetching customers."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

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
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        serializer = CustomerRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            customer = serializer.save()
            return Response({
                "message": "Customer registered successfully!", "data" : serializer.data,

            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GoogleLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Try to get token from both request body and Authorization header
        token = request.data.get('token')

        if not token:
            auth_header = request.headers.get('Authorization', '')
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return Response(
                {"error": "No Google token provided in request body or Authorization header"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get Google Client ID from settings
        google_client_id = getattr(settings, "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", None)
        if not google_client_id:
            return Response(
                {"error": "Google Client ID is not set in settings"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        try:
            # Verify the Google token
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                google_client_id
            )

            # Verify token issuer
            if idinfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
                return Response({"error": "Invalid token issuer"}, status=status.HTTP_400_BAD_REQUEST)

            # Extract user information
            email = idinfo.get('email')
            if not email:
                return Response(
                    {"error": "Email not found in Google token"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Get additional user info
            name = idinfo.get('name', '')
            given_name = idinfo.get('given_name', '')


            # Get or create user
            user, created = User.objects.get_or_create(
                email=email,
                defaults={
                    'name': name or given_name,
                    'is_active': True,
                }
            )

            # Generate JWT tokens using Simple JWT
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response_data = {
                'access_token': access_token,
                'refresh_token': str(refresh),
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'name': user.name,
                },
                'created': created
            }

            # Include customer_code if available
            if hasattr(user, 'customer_code'):
                response_data['user']['customer_code'] = user.customer_code

            return Response(response_data, status=status.HTTP_200_OK)

        except ValueError as e:
            return Response(
                {'error': f"Token verification failed: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': f"Unexpected error: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR

            )
class CustomerDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
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
    permission_classes = [IsAuthenticated]
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)
class OrderCreateAPIView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
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
    permission_classes = [IsAuthenticated]
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


