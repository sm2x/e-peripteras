#!/usr/bin/env python
# -*- coding: utf-8 -*-
from rest_framework import serializers
from rest_framework import fields

from django.utils.translation import ugettext_lazy as _

from peripteras.kiosks.models import Kiosk, Item

import simplejson, urllib





class KioskSerializer(serializers.ModelSerializer):
    """Definition of Serializer for search API json result. _(u'Brand name') """


    def to_representation(self, obj):
        
        # user_address = 'Ηπείρου,1,Καβάλα'
        # kiosk_address = 'Ομονοίας,50,Καβάλα'
        
        f_distances = self.context.get("f_distances")
        f_times = self.context.get("f_times")
        
        kiosk_address = _(u'{0},{1},{2}'.format(obj.street, obj.number, obj.city))

        return {
            'id': obj.id,
            'address': kiosk_address,
            'imageLink': obj.get_image_url(),
            'formatedTime': f_times[obj.id],
            'formatedDistance': f_distances[obj.id],
            'title': obj.title
            # 'raw_time': raw_time,
            # 'raw_distance': raw_distance,
        }
    
    class Meta:
        model = Kiosk


class ItemkSerializer(serializers.ModelSerializer):
    """Definition of Serializer for search API json result."""

    def to_representation(self, obj):
        return {
            'id': obj.id,  
            'name': obj.title,
            'price': obj.price,
            'onlineOffer': obj.online_offer,  
            'category': obj.category.title,
            'KioskId': obj.kiosk.id,
            'brand': obj.brand.title        
        }
    
    class Meta:
        model = Item
