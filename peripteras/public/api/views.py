import re
import simplejson, urllib

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.db.models import Q, FieldDoesNotExist

from django.utils.translation import ugettext_lazy as _

from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import detail_route
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import generics, status, mixins, viewsets

from peripteras.kiosks.models import Kiosk, Item
from peripteras.public.api.serializers import KioskSerializer, ItemkSerializer

from peripteras.common.mixins import FilterMixin

class ReadOnlyKiosksAPIView(FilterMixin,viewsets.ReadOnlyModelViewSet):
	"""
	Endpoint for custom searching about products
	"""
	# authentication_classes = (SessionAuthentication, )
	# permission_classes = (IsAuthenticated, )

	serializer_class = KioskSerializer

	# filter_fields = (
	# 	'category__slug','description__brand__title',
	# 	'description__price',
	# 	'description__price__gte', # Greater than or equal 
	# 	'description__price__lte', # Less than or equal
	# 	'description__needs_service', # use 0 or 1
	# 	'description__service_passed', # use 0 or 1
	# 	'description__guarantee_end_date', 
	# 	'description__city', 
	# )

	# queryset = Product.objects.all()
	
	def get_distance(self, user_address, kiosk_address):
		# returns distance in meters
		url = 'https://maps.googleapis.com/maps/api/distancematrix/json?units=metric&origins={0}&destinations={1}&language=el&key=AIzaSyAp2O-PeL5sjEWf92yJF5umKMPz94_YT4Q'.format(kiosk_address,user_address)

		result= simplejson.load(urllib.urlopen(url))
		raw_distance = result['rows'][0]['elements'][0]['distance']['value']
		raw_time = result['rows'][0]['elements'][0]['duration']['value']
		
		time = result['rows'][0]['elements'][0]['duration']['text']
		distance = result['rows'][0]['elements'][0]['distance']['text']


		return raw_distance, raw_time, distance, time

	def list(self, request):

		try:
			kiosks = Kiosk.objects.filter(activated=True, is_open=True)
		except SuspiciousOperation:
			content = {'please move along': 'nothing to see here'}
			return Response(content, status=status.HTTP_400_BAD_REQUEST)
			
		kiosks = self.apply_filters(request, kiosks)

		available_kiosks = []
		f_distances = {}
		f_times = {}
		
		user_address = _(u'{0}'.format(request.session.get('user_address', None)))

		if not user_address:
			data = {
				'error':'No address'
			}
			return Response(data, status=status.HTTP_200_OK)

		for ksk in kiosks:
			tmp_adr = _(u'{0},{1},{2}'.format(ksk.street, ksk.number, ksk.city))
			distance, time, formatet_time, formated_distance = self.get_distance(user_address, tmp_adr)

			distance =  distance/1000
			if distance < ksk.max_distance:

				f_distances[ksk.id] = formated_distance
				f_times[ksk.id] = formatet_time

				available_kiosks.append(ksk)

		serializer = self.serializer_class(available_kiosks, many=True,
															context={
																'f_distances': f_distances,
																'f_times':f_times
															}
										)
		return Response(serializer.data, status=status.HTTP_200_OK)
		


class ReadOnlyKioskItemsAPIView(FilterMixin,viewsets.ReadOnlyModelViewSet):

	# Get items from kiosk
	# http://localhost:8001/api/kiosk/items/?kiosk_id=4&online_offer=1
	# 
	serializer_class = ItemkSerializer

	filter_fields = (
		'kiosk_id', 'kiosk__city',
		'online_offer', 'category__slug'
	)

	def list(self, request):

			try:
				items = Item.objects.all()
			except SuspiciousOperation:
				content = {'please move along': 'nothing to see here'}
				return Response(content, status=status.HTTP_400_BAD_REQUEST)
				
			items = self.apply_filters(request, items)

			serializer = self.serializer_class(items, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)