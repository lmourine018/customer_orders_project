from rest_framework import serializers
from customer_order_app.models import Customer, Order

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
        fields = ['id', 'customer', 'customer_id', 'item', 'amount', 'created_at', 'status','order_number']
        extra_kwargs = {
            'order_number': {'required': False},
        }

    def create(self, validated_data):
        # Explicitly extract customer from validated_data
        customer = validated_data.pop('customer', None)
        order = Order.objects.create(customer=customer, **validated_data)
        return order

    def update(self, instance, validated_data):
        # Handle customer_id if provided
        if 'customer_id' in validated_data:
            instance.customer_id = validated_data.pop('customer_id')

        # Normalize status to uppercase
        if 'status' in validated_data:
            validated_data['status'] = validated_data['status'].upper()

        # Explicitly update each field
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.full_clean()  # This will run model-level validations
        instance.save()
        return instance

    def validate(self, data):
        # Additional validation logic
        if 'status' in data:
            valid_statuses = ['PENDING', 'PROCESSED', 'SHIPPED']
            status = data['status'].upper()
            if status not in valid_statuses:
                raise serializers.ValidationError({
                    'status': f"Invalid status. Choose from {valid_statuses}"
                })
        return data


class CustomerRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = Customer
        fields = ['id','name', 'customer_code', 'email', 'phone_number', 'password']

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
