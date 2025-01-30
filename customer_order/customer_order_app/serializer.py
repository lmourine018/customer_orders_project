from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import Customer,Order

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'name', 'customer_code', 'email', 'phone_number', 'created_at']

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

    def create(self, validated_data):
        # handling customer property
        customer = validated_data.pop('customer', None)
        order = Order.objects.create(customer=customer, **validated_data)
        return order


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Customer
        fields = ['name', 'customer_code', 'email', 'phone_number', 'password']

    def create(self, validated_data):
        # Hash the password before saving
        password = validated_data.pop('password')
        customer = Customer.objects.create(**validated_data)
        customer.set_password(password)
        customer.save()
        return customer

    def validate_email(self, value):
        if Customer.objects.filter(email=value).exists():
            raise serializers.ValidationError("A customer with this email already exists.")
        return value

    def validate_code(self, value):
        if Customer.objects.filter(customer_code=value).exists():
            raise serializers.ValidationError("A customer with this code already exists.")
        return value
