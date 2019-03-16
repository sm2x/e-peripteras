#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from collections import Counter

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
from peripteras.users.api.serializers import BasketSerializer

from peripteras.common.mixins import FilterMixin


class AddToBasket(FilterMixin, generics.CreateAPIView):
    """
    Endpoint for adding items to basket
    http://localhost:8001/user/api/basket/add/
    """

    # authentication_classes = (SessionAuthentication, )
    # permission_classes = (IsAuthenticated, )
    # queryset = Item.objects.all()

    serializer_class = ItemkSerializer

    def get(self, request):
        item_id = request.GET.get("item_id", None)
        kiosk_id = request.GET.get("kiosk_id", None)
        # basket = request.session.get('basket', None)
        kiosk_ids = []

        orders_holder = request.session.get('orders_holder', None)

        if item_id and kiosk_id:
            if orders_holder:
                # users has at least one order
                for order in orders_holder:
                    kiosk_ids.append(order['kiosk'])

                if kiosk_id in kiosk_ids:
                    for order in orders_holder:
                        if order['kiosk'] == kiosk_id:
                            # 'this kiosk has items, add item to item list'
                            order['items'].append(item_id)

                            orders_holder_tmp = request.session.get(
                                'orders_holder', None)
                            orders_holder_tmp.append(order)
                            request.session[
                                'orders_holder'] = orders_holder_tmp

                            # remove this order from session
                            orders_holder.remove(order)

                            data = {
                                'msg': 'Προστέθηκε στο καλάθι'
                            }
                            return Response(data, status=status.HTTP_200_OK)
                else:
                    # create new order for new kiosk
                    items_list = [item_id]
                    order = {
                        'kiosk': kiosk_id,
                        'items': items_list
                    }
                    tmp_orders_holder = orders_holder
                    tmp_orders_holder.append(order)
                    request.session['orders_holder'] = tmp_orders_holder
                    data = {
                        'msg': 'Νέα παραγελία. Μπήκε στο καλάθι'
                    }
                    return Response(data, status=status.HTTP_200_OK)
            else:
                # init the orders sesion holder
                request.session['orders_holder'] = []

                # create an order dict
                items_list = [item_id]
                order = {
                    'kiosk': kiosk_id,
                    'items': items_list
                }

                tmp_orders_holder = request.session.get('orders_holder', None)
                tmp_orders_holder.append(order)
                request.session['orders_holder'] = tmp_orders_holder

                data = {
                    'msg': 'Μπήκε το πρώτο αντικείμενο στο καλάθι'
                }
                return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'msg': 'error no kiosk item id'
            }
            return Response(data, status=status.HTTP_406_NOT_ACCEPTABLE)

        # order = {
        # 	'kiosk':kiosk_id,
        # 	'items':basket
        # }

        # # order_init = ['order1','order2']

        # # request.session['orders'] = order_init

        # tmp_orders = request.session.get('orders', None)
        # tmp_orders.append(order)
        # request.session['orders'] = tmp_orders

        # item_to_add = Item.objects.get(id=item_id)

        # if basket:
        # 	basket = request.session['basket']
        # 	basket.append(item_to_add.id)
        # 	request.session['basket'] = basket
        # else:
        # 	basket = []
        # 	basket.append(item_to_add.id)
        # 	request.session['basket'] = basket

        data = {
            'msg': 'whaat'
        }
        return Response(data, status=status.HTTP_200_OK)


class GetFromBasket(FilterMixin, generics.CreateAPIView):
    """
    Endpoint for fetching the basket
    http://localhost:8001/user/api/basket/get/
    """

    # authentication_classes = (SessionAuthentication, )
    # permission_classes = (IsAuthenticated, )
    # queryset = Item.objects.all()

    serializer_class = BasketSerializer

    def get(self, request):

        kiosk_id = request.GET.get("kiosk_id", None)
        orders_holder = request.session.get('orders_holder', None)
        basket_items_ids = None

        if orders_holder:
            for order in orders_holder:
                if order['kiosk'] == kiosk_id:
                    basket_items_ids = order['items']
        # else:
        # 	data = {
        # 		'msg':'Άδειο καλάθι'
        # 	}
        # 	return Response(data, status=status.HTTP_200_OK)

        # basket_items_ids = request.session.get('basket', None)
        kiosk = Kiosk.objects.get(id=kiosk_id)
        basket_items = []
        ziped_data = []
        total_price = 0

        if basket_items_ids:
            for it_id in basket_items_ids:
                tmp_item = Item.objects.get(id=it_id)
                total_price += tmp_item.price

                basket_items.append(tmp_item)

            fee = Item()
            fee.price = kiosk.delivery_fee
            fee.title = _(u'Έξοδα μεταφοράς')
            fee.id = False
            basket_items.append(fee)

            unique_items = Counter(basket_items)

            ziped_data = zip(unique_items.keys(), unique_items.values())

        ziped_data = self.apply_filters(request, ziped_data)

        serializer = self.serializer_class(ziped_data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RemoveFromBasket(FilterMixin, generics.CreateAPIView):
    """
    Endpoint for removing items from basket
    http://localhost:8001/user/api/basket/remove/
    """

    # authentication_classes = (SessionAuthentication, )
    # permission_classes = (IsAuthenticated, )
    # queryset = Item.objects.all()

    serializer_class = ItemkSerializer

    def get(self, request):
        item_id = request.GET.get("item_id", None)
        kiosk_id = request.GET.get("kiosk_id", None)

        orders_holder = request.session.get('orders_holder', None)

        basket = request.session.get('basket', None)

        # if item_id:
        # 	item_id = int(item_id)
        # Here we get unicode, convert it to int to find inbasket type = (list)

        if orders_holder:
            for order in orders_holder:
                if order['kiosk'] == kiosk_id:
                    if item_id not in order['items']:
                        data = {
                            'msg': 'Δεν ηταν στο καλάθι'
                        }
                        return Response(data, status=status.HTTP_200_OK)

                    order['items'].remove(item_id)

                    orders_holder_tmp = request.session.get(
                        'orders_holder', None)

                    orders_holder_tmp.append(order)
                    request.session['orders_holder'] = orders_holder_tmp

                    # remove this order from session
                    orders_holder.remove(order)

                    data = {
                        'msg': 'Aφαιρέθηκε από το καλάθι'
                    }
                    return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'msg': 'Άδειο καλάθι'
            }
            return Response(data, status=status.HTTP_200_OK)
