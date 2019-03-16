from rest_framework import serializers
from peripteras.kiosks.models import Kiosk, Item


class KioskSerializer(serializers.ModelSerializer):
    """Definition of Serializer for search API json result."""

    def to_representation(self, obj):
        return {
            'id': obj.id,
            'time': obj.time,
            'distance': obj.distance
        }

    class Meta:
        model = Kiosk


class BasketSerializer(serializers.ModelSerializer):

    def to_representation(self, obj):
        tmp_item = obj[0]
        # print type(tmp_item)
        return {
            'name': tmp_item.title,
            'times': obj[1],
            'price': format(tmp_item.price, '.2f'),
            'id': tmp_item.id
        }

    class Meta:
        model = Item
