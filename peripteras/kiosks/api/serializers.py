from rest_framework import serializers

from peripteras.users.models import Order


class OrderSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        return {
            'street': obj.address.street,
            'number': obj.address.number,
            'city': obj.address.city,
            'region': obj.address.region,
            'orderId': obj.id,
            'totalSum': obj.total_sum,
            'created': obj.created_on.strftime('%Y-%m-%d %H:%M:%S'),
            'fullName': obj.full_name(),

        }

    class Meta:
        model = Order
