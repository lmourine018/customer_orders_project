from rest_framework import serializers
from .models import Customer,Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'code', 'email', 'phone_number', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(),
        source='customer',
        write_only=True
    )

    class Meta:
        model = Order
        fields = ['id', 'customer', 'customer_id', 'item', 'amount', 'created_at', 'status']