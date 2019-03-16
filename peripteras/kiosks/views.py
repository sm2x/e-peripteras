#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import codecs
import csv


from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect


from peripteras.users.models import Order
from peripteras.kiosks.models import Item, Kiosk, KioskManager, Brand, Category

import peripteras.kiosks.forms as forms


@login_required
def kiosk(request):

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        orders = Order.objects.filter(kiosk=kiosk, completed=False)

        data = {
            'kiosk': kiosk,
            'orders': orders,
        }

        return render(request, 'kiosk-managers/home.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def help(request):

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        support_form = forms.SupportForm(request.POST or None)

        if support_form.is_valid():
            support = support_form.save(commit=False)
            support.kiosk = kiosk
            support.manager = manager
            support.save()

            txt = u'Θα επικοινωνήσουμε σύντομα μαζί σας'

            data = {
                'kiosk': kiosk,
                'txt': txt
            }

            return render(request, 'kiosk-managers/finished.html', data)

        data = {
            'kiosk': kiosk,
            'support_form': support_form,
        }

        return render(request, 'kiosk-managers/help.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def kiosk_info(request):
    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        kiosk_info = forms.KioskForm(
            request.POST or None, request.FILES or None, instance=kiosk)

        if kiosk_info.is_valid():
            kiosk = kiosk_info.save(commit=False)
            kiosk.save()
            return redirect('managers:kiosk_dashboard')

        data = {
            'kiosk_info': kiosk_info,
            'kiosk': kiosk,
        }

        return render(request, 'kiosk-managers/kiosk_info.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def all_items(request):
    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        order = request.GET.get('order_by', None)

        if order == 'price' or order == 'brand' or order == 'category' or order == 'id' or order == 'online_offer':
            items = Item.objects.filter(kiosk=kiosk).order_by(order)
        else:
            items = Item.objects.filter(kiosk=kiosk).order_by('-created_on')

        items_offer = 0
        for it in items:
            if it.online_offer:
                items_offer += 1

        paginator = Paginator(items, 100)
        page = request.GET.get('page', 1)

        try:
            items_paginated = paginator.page(page)
        except PageNotAnInteger:
            items_paginated = paginator.page(1)
        except EmptyPage:
            items_paginated = paginator.page(1)

        data = {
            'items_all': items,
            'items': items_paginated,
            'items_offer': items_offer,
            'kiosk': kiosk,
        }

        return render(request, 'kiosk-managers/items.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def item_edit(request, item_id):

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        item = Item.objects.get(id=item_id, kiosk=kiosk)

        item_edit = forms.ItemForm(request.POST or None,
                                   request.FILES or None, instance=item)

        if item_edit.is_valid():
            item = item_edit.save(commit=False)
            item.save()

            return redirect('managers:all_items')

        data = {
            'item': item,
            'kiosk': kiosk,
            'item_edit': item_edit
        }

        return render(request, 'kiosk-managers/item_edit.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def item_add(request):

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        item = Item()

        item_add = forms.ItemForm(request.POST or None,
                                  request.FILES or None, instance=item)

        if item_add.is_valid():
            item = item_add.save(commit=False)
            item.kiosk = kiosk
            item.save()

            return redirect('managers:all_items')

        data = {
            'item': item,
            'kiosk': kiosk,
            'item_add': item_add
        }

        return render(request, 'kiosk-managers/item_add.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def item_delete(request, item_id):

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager and item_id:
        kiosk = manager.kiosk

        item = Item.objects.get(id=item_id, kiosk=kiosk)
        item.delete()

        txt = u'Το προϊόν διαγράφηκε.'

        data = {
            'kiosk': kiosk,
            'order': order,
            'txt': txt
        }

        return render(request, 'kiosk-managers/finished.html', data)

        data = {
            'item': item,
            'kiosk': kiosk,
            'item_add': item_add
        }

        return render(request, 'kiosk-managers/item_add.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def order(request, order_id):

    items_objs = []

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        order = Order.objects.get(id=order_id, kiosk=kiosk)

        jsonDec = json.decoder.JSONDecoder()
        items_list_ids = jsonDec.decode(order.basket_items_ids)

        for item_id in items_list_ids:
            tmp_item = Item.objects.get(id=item_id)
            items_objs.append(tmp_item)

        data = {
            'kiosk': kiosk,
            'order': order,
            'order_items': items_objs
        }

        return render(request, 'kiosk-managers/order.html', data)
    else:
        return HttpResponseForbidden()


@login_required
def complete_order(request, order_id):
    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        order = Order.objects.get(id=order_id, kiosk=kiosk)

        order.completed = True
        order.save()
        txt = u'Η παραγγελία έκλεισε'

        data = {
            'kiosk': kiosk,
            'order': order,
            'txt': txt
        }

        return render(request, 'kiosk-managers/finished.html', data)
    else:
        return HttpResponseForbidden()


def _csv_unireader(f, encoding='utf-8'):
    return csv.DictReader(
        codecs.iterencode(codecs.iterdecode(f, encoding), 'utf-8'),
        delimiter=',')


@login_required
def upload_list(request):

    try:
        manager = KioskManager.objects.get(user=request.user)
    except KioskManager.DoesNotExist:
        manager = None

    if request.user.is_authenticated() and manager:
        kiosk = manager.kiosk

        upload_form = forms.CSVImportForm(request.POST or None,
                                          request.FILES or None,
                                          kiosk=Kiosk.objects.filter(kioskmanager=manager))

        if upload_form.is_valid():

            input_type = upload_form.cleaned_data['input_type']
            uploaded_file = upload_form.cleaned_data['uploaded_file']
            if input_type == 'csv':
                data_rows = _csv_unireader(uploaded_file)

            saved = 0

            for row in data_rows:

                if row['price']:
                    price = row['price']

                if row['title']:
                    title = row['title'].decode('utf-8')

                if row['brand']:
                    brand_tmp = row['brand'].decode('utf-8')
                    brands = Brand.objects.all().values_list('title', flat=True)

                    if brand_tmp in brands:
                        brand = Brand.objects.get(title=brand_tmp)
                    else:
                        brand = Brand.objects.create(title=brand_tmp)

                if row['category']:
                    cat_tmp = row['category'].decode('utf-8')
                    cats = Category.objects.all().values_list('title', flat=True)

                    if cat_tmp in cats:
                        cat = Category.objects.get(title=cat_tmp)
                    else:
                        cat_obj = Category.objects.create(title=cat_tmp)
                        cat = cat_obj

                item = Item.objects.update_or_create(
                    price=price,
                    title=title,
                    brand=brand,
                    category=cat,
                    kiosk=kiosk)

                saved += 1

            data = {
                'kiosk': kiosk,
                'upload_form': upload_form,
                'saved': saved
            }
            return render(request, 'kiosk-managers/upload.html', data)

        data = {
            'kiosk': kiosk,
            'upload_form': upload_form,
        }
        return render(request, 'kiosk-managers/upload.html', data)
    else:
        return HttpResponseForbidden()
