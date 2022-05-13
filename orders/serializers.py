from rest_framework import serializers
from delivery_person.models import DeliveryPerson

from orders.models import Order, OrderItem


class AcceptedBySerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.full_name', read_only=True)
    mobile = serializers.CharField(source='user.mobile', read_only=True)

    class Meta:
        model = DeliveryPerson
        fields = ('full_name', 'mobile')

class OrderItemSerializer(serializers.ModelSerializer):
    # url = serializers.HyperlinkedIdentityField(view_name="order:order_item")
    food_name = serializers.CharField(source='food.name', read_only=True)
    quantity = serializers.IntegerField(min_value=1)
    price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    restaurant_name = serializers.CharField(source='food.restaurant.user.full_name', read_only=True)
    # restaurant_id = serializers.IntegerField(source='food.restaurant.id', read_only=True)
    
    class Meta:
        model = OrderItem
        exclude = ('created', 'updated', 'order', 'id')


class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    status = serializers.ChoiceField(choices=Order.STATUS_CHOICES, read_only=True)
    accepted_by = AcceptedBySerializer(read_only=True)
    accepted_on = serializers.DateTimeField(read_only=True)
    is_accepted = serializers.BooleanField(read_only=True)

    class Meta:
        model = Order
        exclude = ('created', 'updated', 'customer')


class DeliveryLocationSerializer(serializers.Serializer):
    latitude = serializers.CharField(max_length=20)
    longitude = serializers.CharField(max_length=20)
    address = serializers.CharField(max_length=500)
    city = serializers.CharField(max_length=100)


