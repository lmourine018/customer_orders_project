from django.http import HttpResponse
from django.views import View
from mozilla_django_oidc.contrib.drf import OIDCAuthentication
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Customer, Order
from .serializer import CustomerSerializer, OrderSerializer

class CustomerListAPIView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data)

class CustomerCreateAPIView(APIView):
    authentication_classes = [OIDCAuthentication]
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

class CustomOIDCErrorView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse("Authentication failed. Please try again.", status=401)

class OrderListAPIView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

class OrderCreateAPIView(APIView):
    authentication_classes = [OIDCAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return Response(
                {"error": "No authorization token provided"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(user = request.user)
                return Response({"message": "Order created successfully!",
               "data" : serializer.data}, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
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
