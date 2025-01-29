# urls.py
from django.urls import path
from .views import CustomerCreateAPIView, CustomerListAPIView, CustomerDetailAPIView, OrderCreateAPIView, \
    OrderListAPIView, OrderDetailAPIView, CustomerRegistrationView, CustomerLoginView, GoogleLoginView

urlpatterns = [
    path('customers/', CustomerCreateAPIView.as_view(), name='customer_order_app-create'),
    path('customers/list', CustomerListAPIView.as_view(), name='customer_order_app-list'),
    path('customers/<int:pk>/', CustomerDetailAPIView.as_view(), name='customer_order_app-detail'),
    path('orders/', OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/list', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
   path('register/', CustomerRegistrationView.as_view(), name='customer-register'),
    path('login/', CustomerLoginView.as_view(), name='customer-login'),
    path('auth/google/', GoogleLoginView.as_view(), name='google-login'),
]
