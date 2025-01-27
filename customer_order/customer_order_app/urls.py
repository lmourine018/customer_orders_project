# urls.py
from django.urls import path
from .views import CustomerCreateAPIView, CustomerListAPIView, CustomerDetailAPIView, OrderCreateAPIView, \
    OrderListAPIView, OrderDetailAPIView, CustomOIDCErrorView
from mozilla_django_oidc.views import OIDCAuthenticationCallbackView

urlpatterns = [
    path('customers/', CustomerCreateAPIView.as_view(), name='customer_order_app-create'),
    path('customers/list', CustomerListAPIView.as_view(), name='customer_order_app-list'),
    path('customers/<int:pk>/', CustomerDetailAPIView.as_view(), name='customer_order_app-detail'),
    path('orders/', OrderCreateAPIView.as_view(), name='order-create'),
    path('orders/list', OrderListAPIView.as_view(), name='order-list'),
    path('orders/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('oidc/callback/', OIDCAuthenticationCallbackView.as_view(), name='oidc-callback'),
    path('oidc/error/', CustomOIDCErrorView.as_view(), name='oidc_error'),
]
