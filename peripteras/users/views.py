#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives


from collections import Counter

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from django.http import HttpResponse, Http404, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect

from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _


from peripteras.users.models import SimpleUser, Order, Addresses, Feedback
from peripteras.kiosks.models import Item, Kiosk, KioskManager

import peripteras.users.forms as forms


@require_POST
@sensitive_post_parameters()
@csrf_protect
def custom_login(request):
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        response_data = {}
        if login_form.is_valid():
            response_data['result'] = 'success'
            response_data['message'] = 'You are logged in'

            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
        else:
            response_data['result'] = 'failed'
            response_data['message'] = 'You messed up'

        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponseForbidden()

# @require_POST
# @sensitive_post_parameters()
# @csrf_protect


def register(request):

    user = User()
    simple_user = SimpleUser()

    user_form = forms.UserForm(request.POST or None, instance=user)
    simple_user_form = forms.SimpleUserForm(
        request.POST or None, instance=simple_user)

    login_form = forms.LoginAuthenticationForm(request.POST or None)

    # if user_form.is_valid() and simple_user_form.is_valid():
    if user_form.is_valid():
        user = user_form.save(commit=False)
        # user.is_active = 0 # not active until he opens activation link
        user.set_password(user.password)
        user.save()

        simple_user = SimpleUser.objects.create(user=user)
        simple_user.save()

        # username= request.POST.get('username')
        # password = request.POST.get('password')
        # user = authenticate(username=username, password=password)
        # if user is not None:
        # 	login(request, user)

        # simple_user = simple_user_form.save(commit=False)

        # # print simple_user.avatar
        # simple_user.user = user

        # salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        # activation_key = hashlib.sha1(salt+user.email).hexdigest()
        # key_expires = datetime.datetime.today() + datetime.timedelta(2)

        # simple_user.activation_key = activation_key
        # simple_user.key_expires = key_expires
        # simple_user.save()

        # Send email with activation key
        text_content = u''
        ctx = {
            'email': user.email,
        }
        template = get_template('mailer.html',
                                using='django')
        context = Context(ctx)
        subject = render_to_string(
            'email_subject.txt',
            ctx, using='django')

        # Email subject * must not* contain newlines
        subject = ''.join(subject.splitlines())

        content = template.render(context)
        message = EmailMultiAlternatives(
            subject, text_content,
            settings.FROM, [user.email])
        message.attach_alternative(content, 'text/html')
        message.content_subtype = "html"
        message.send()

        msg = _(u'Η εγγραφή ολοκληρώθηκε, μπορείς να συνεχίσεις.')
        title = _(u'Εγραφή')

        data = {
            'title': title,
            'msg': msg
        }
        return render(request, 'users/success.html', data)

    data = {
        'simple_user_form': simple_user_form,
        'user_form': user_form,
        'form': login_form
    }
    return render(request, 'users/login.html', data)


def register_manager(request):

    user = User()
    user_form = forms.UserManagerForm(request.POST or None, instance=user)
    manager_form = forms.ManagerForm(request.POST or None)
    kiosk_form = forms.KioskForm(request.POST or None)

    # if user_form.is_valid() and simple_user_form.is_valid():
    if user_form.is_valid() and manager_form.is_valid() and kiosk_form.is_valid():
        user = user_form.save(commit=False)
        manager = manager_form.save(commit=False)
        kiosk = kiosk_form.save(commit=False)

        user.is_active = 0  # not active
        user.set_password(user.password)
        user.save()

        kiosk_obj = Kiosk.objects.create(street=kiosk.street, number=kiosk.number,
                                         city=kiosk.city, tk=kiosk.tk, activated=False)
        kiosk_obj.save()

        kiosk_manager = KioskManager.objects.create(
            user=user, birth_date=manager.birth_date, kiosk=kiosk_obj,
            mobile_number=manager.mobile_number, email=user.email)

        kiosk_manager.save()

        msg = _(
            u'Η αίτηση για περίπτερο ολοκληρώθηκε. Θα επικοινωνήσουμε μαζί σας σύντομα.')
        title = _(u'Εγραφή περιπτέρου')

        data = {
            'title': title,
            'msg': msg
        }
        return render(request, 'users/success.html', data)

    data = {
        # 'simple_user_form': simple_user_form,
        'user_form': user_form,
        'manager_form': manager_form,
        'kiosk_form': kiosk_form
    }
    return render(request, 'users/register-manager.html', data)


@login_required
def basket(request, kiosk_id):

    basket_items_ids = request.session.get('basket', None)

    kiosk = Kiosk.objects.get(id=kiosk_id)

    basket_items = []
    ziped_data = []
    total_price = 0
    simple_user = None

    if request.user.is_authenticated():
        simple_user = SimpleUser.objects.get(user__username=request.user)

    orders_holder = request.session.get('orders_holder', None)
    basket_items_ids = None

    if orders_holder:
        for order in orders_holder:
            if order['kiosk'] == kiosk_id:
                basket_items_ids = order['items']

    if basket_items_ids:
        for it_id in basket_items_ids:
            tmp_item = Item.objects.get(id=it_id)
            total_price += tmp_item.price

            basket_items.append(tmp_item)

        unique_items = Counter(basket_items)
        ziped_data = zip(unique_items.keys(), unique_items.values())

    data = {
        'kiosk': kiosk,
        'simple_user': simple_user,
        'basket_items': ziped_data,
        'total_price': total_price,
    }

    return render(request, 'users/basket.html', data)


@login_required
@require_POST
def completed(request, kiosk_id):

    kiosk = Kiosk.objects.get(id=kiosk_id)

    if request.user.is_authenticated():
        simple_user = SimpleUser.objects.get(user__username=request.user)

    orders_holder = request.session.get('orders_holder', None)
    basket_items_ids = None
    items_objs = []
    total_sum = 0
    comments = request.POST.get('comments', None)
    order_firstname = request.POST.get(
        'order_firstname', simple_user.first_name)
    order_lastname = request.POST.get('order_lastname', simple_user.last_name)
    mobile_number = request.POST.get(
        'mobile_number', simple_user.mobile_number)

    city = request.POST.get('city', None)
    region = request.POST.get('region', None)
    street = request.POST.get('street', None)
    area_number = request.POST.get('area_number', None)
    tk = request.POST.get('tk', None)

    order_addr = Addresses.objects.create(street=street,
                                          number=area_number,
                                          city=city,
                                          region=region,
                                          tk=tk,
                                          simple_user_id=simple_user.id)

    if not simple_user.addresses:
        simple_user.addresses = order_addr
        simple_user.save()

    if not simple_user.first_name:
        simple_user.first_name = order_firstname
        simple_user.save()

    if not simple_user.last_name:
        simple_user.last_name = order_lastname
        simple_user.save()

    if not simple_user.mobile_number:
        simple_user.mobile_number = mobile_number
        simple_user.save()

    # get items from basket
    if orders_holder:
        for order in orders_holder:
            if order['kiosk'] == kiosk_id:
                basket_items_ids = order['items']

    if not basket_items_ids:
        return redirect('users:basket', kiosk_id)

    for it_id in basket_items_ids:
        # save the total sum
        tmp_item = Item.objects.get(id=it_id)
        total_sum = total_sum + tmp_item.price

        items_objs.append(tmp_item)

    # create the order
    total_sum = total_sum + kiosk.delivery_fee

    order = Order.objects.create(simple_user=simple_user, kiosk=kiosk,
                                 total_sum=total_sum, address=order_addr,
                                 first_name=order_firstname,
                                 last_name=order_lastname,
                                 mobile_number=mobile_number,
                                 comments=comments,
                                 basket_items_ids=json.dumps(basket_items_ids))

    order.save()

    # add unique items
    # for itm in items_objs:
    # 	order.basket_items.add(itm)

    # conect order to simple_user for latter use
    simple_user.orders.add(order)
    simple_user.save()

    data = {
        'simple_user': simple_user,
        'kiosk': kiosk,
        'order': order
    }

    return render(request, 'users/completed.html', data)


@login_required
def add_feedback(request, order_id):

    simple_user = SimpleUser.objects.get(user=request.user)
    order = Order.objects.get(id=order_id, simple_user=simple_user)

    if Feedback.objects.filter(simple_user=simple_user, order=order).exists():
        return redirect('public:kiosk', order.kiosk.id)

    feedback_form = forms.FeedbackForm(request.POST or None)

    if feedback_form.is_valid():

        feedback = feedback_form.save(commit=False)
        feedback.simple_user = simple_user
        feedback.order = order
        feedback.save()

        msg = _(u'Η αξιολόγηση προστέθηκε.')
        title = _(u'Αξιολόγηση')

        data = {
            'title': title,
            'msg': msg,
            'kiosk': order.kiosk
        }

        return render(request, 'users/feedback_success.html', data)

    data = {
        'order': order,
        'feedback_form': feedback_form
    }

    return render(request, 'users/add_feedback.html', data)
