#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import re

from collections import Counter

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.db.models import Q, FieldDoesNotExist


from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, mixins, viewsets

from peripteras.kiosks.models import Kiosk, Item
from peripteras.public.api.serializers import KioskSerializer, ItemkSerializer
from peripteras.kiosks.api.serializers import OrderSerializer

from peripteras.common.mixins import FilterMixin

from peripteras.users.models import Order

from peripteras.kiosks.models import KioskManager

		

class GetAllOrders(FilterMixin,generics.CreateAPIView):
	"""
	Endpoint for fetching the basket
	http://localhost:8001/user/api/basket/get/
	"""


	authentication_classes = (SessionAuthentication, )
	permission_classes = (IsAuthenticated, )
	# queryset = Item.objects.all()

	filter_fields = (
		'kiosk_id'
	)


	serializer_class = OrderSerializer

	def get(self, request):
		
		kiosk_id = request.GET.get("kiosk_id", None)

		try:
			kiosk = Kiosk.objects.get(id=kiosk_id, kioskmanager__user=request.user)
		except Kiosk.DoesNotExist:

			data={
				'error':'403 FORBIDDEN',
				'msg': 'No cheats...' 
			}
			return Response(data, status=status.HTTP_403_FORBIDDEN)
		   
		


		orders = Order.objects.filter(kiosk=kiosk_id, completed=False).order_by('created_on')
			
		orders = self.apply_filters(request, orders)

		serializer = self.serializer_class(orders, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)


