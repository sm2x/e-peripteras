#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import random
from collections import Counter
from django.http import Http404
from django.shortcuts import get_object_or_404, render, redirect

# from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

# from django.views.decorators.http import require_POST

from peripteras.users.models import SimpleUser, Feedback
from peripteras.kiosks.models import Kiosk, Item, KioskManager, Category

# import peripteras.public.forms as forms

from django.conf import settings
from django.template import Context
from django.template.loader import render_to_string, get_template
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _


def _clean_search_post(data):
    """Ensure data are valid."""
    if not re.match(r'(^[\w\s.]+$)', data, re.UNICODE):
        return None
    return data


def home(request):
    """
    home page
    """

    # user = User()
    # simple_user = SimpleUser()

    # user_form = forms.UserForm(request.POST or None, instance=user)
    # simple_user_form = forms.SimpleUserForm(request.POST or None,
    #                                       request.FILES or None, instance=simple_user)

    # if user_form.is_valid() and simple_user_form.is_valid():
    #   print 'valid form'
    #   user = user_form.save(commit=False)
    #   user.set_password(user.password)
    #   user.save()

    #   simple_user = simple_user_form.save(commit=False)
    #   simple_user.user = user
    #   simple_user.save()

    #   print 'valid registration'

    manager = None
    if request.user.is_authenticated():
        try:
            manager = KioskManager.objects.get(user=request.user)
        except KioskManager.DoesNotExist:
            manager = None

    data = {
        'manager': manager
    }
    return render(request, 'public/home.html', data)


# def first_step(request):
#   # login - register page
#   # if request.user.is_authenticated():
#   #   return redirect('public:second_step')

#   data = {
#   }
#   return render(request, 'public/first-step.html', data)

def areas(request):

    data = {
    }
    return render(request, 'public/areas.html', data)


def zoho(request):

    data = {
    }
    return render(request, 'public/verifyforzoho.html', data)


@login_required
def second_step(request):
    simple_user = SimpleUser.objects.get(user__username=request.user)

    request.session['city'] = request.POST.get("city", None)
    request.session['area'] = request.POST.get("area", None)
    request.session['street'] = request.POST.get("street", None)
    request.session['area_number'] = request.POST.get("area_number", None)

    data = {
        'simple_user': simple_user
    }
    return render(request, 'public/second-step.html', data)

# # @login_required
# # @require_POST
# def all_kiosks(request):
#   #  select kiosk
#   print 'request.method'
#   if request.method == "POST":
#       # request.session['city'] = request.POST.get("city", None)
#       # request.session['area'] = request.POST.get("area", None)
#       # request.session['street'] = request.POST.get("street", None)
#       # request.session['area_number'] = request.POST.get("area_number", None)

#       print 'POST HERE'


#   data = {
#   }
#   return render(request, 'public/third-step.html', data)

def kiosk(request, id):
    if request.user.is_authenticated():
        simple_user = SimpleUser.objects.get(user__username=request.user)
    else:
        simple_user = None

    kiosk = get_object_or_404(Kiosk, id=id)
    items = Item.objects.filter(kiosk=kiosk)

    feedbacks = Feedback.objects.filter(order__kiosk=kiosk)

    stars = 0
    for fd in feedbacks:
        stars += fd.stars

    if stars:
        avg = stars / feedbacks.count()
    else:
        avg = 0

    basket_items_ids = request.session.get('basket', None)

    basket_items = []
    ziped_data = []
    total_price = 0

    if basket_items_ids:
        for it_id in basket_items_ids:
            tmp_item = Item.objects.get(id=it_id)
            total_price += tmp_item.price

            basket_items.append(tmp_item)

        unique_items = Counter(basket_items)
        ziped_data = zip(unique_items.keys(), unique_items.values())

    kiosk_cats = []

    cats_ids = items.distinct('category').values_list('category', flat=True)

    for cat_id in cats_ids:
        kiosk_cats.append(Category.objects.get(id=cat_id))
    data = {
        'kiosk': kiosk,
        'items': items,
        'basket_items': ziped_data,
        'total_price': total_price,
        'simple_user': simple_user,
        'feedbacks': feedbacks,
        'kiosk_cats': kiosk_cats,
        'avg': avg
    }
    return render(request, 'public/kiosk.html', data)


def all_kiosks(request):

    # kiosks = Kiosk.objects.all()

    if request.method == "POST":

        request.session['user_address'] = request.POST.get(
            "user_address", None)
        # request.session['area'] = request.POST.get("area", None)
        # request.session['street'] = request.POST.get("street", None)
        # request.session['area_number'] = request.POST.get("area_number", None)

        print 'POST HERE'

    data = {
        # 'kiosks':kiosks,
    }
    return render(request, 'public/all_kiosks.html', data)


def contact(request):

    if request.POST:
        f_name = request.POST.get('f_name', None)
        l_name = request.POST.get('l_name', None)
        contact_email = request.POST.get('email', None)
        number = request.POST.get('number', None)
        form_msg = request.POST.get('form_msg', None)

        if contact_email and form_msg:

            text_content = u''
            ctx = {
                'email': contact_email,
                'f_name': f_name,
                'l_name': l_name,
                'number': number,
                'form_msg': form_msg,
            }
            template = get_template('mail_to_admin.html',
                                    using='django')
            context = Context(ctx)
            subject = render_to_string(
                'email_to_admin_subject.txt',
                ctx, using='django')

            # Email subject * must not* contain newlines
            subject = ''.join(subject.splitlines())

            content = template.render(context)
            message = EmailMultiAlternatives(
                subject, text_content,
                settings.FROM, ['info@e-peripteras.gr'])
            message.attach_alternative(content, 'text/html')
            message.content_subtype = "html"
            message.send()

            msg = _(
                u'Ευχαριστούμε για το μήνυμα, σύντομα θα επικοινωνήσουμε μαζί σου.')
            title = _(u'Επικοινωνία')

            data = {
                'title': title,
                'msg': msg
            }
            return render(request, 'users/success.html', data)

    data = {

    }
    return render(request, 'public/contact.html', data)


def how(request):

    data = {
    }
    return render(request, 'public/how.html', data)


def terms(request):

    data = {
    }
    return render(request, 'public/terms.html', data)


def faq(request):

    data = {
    }
    return render(request, 'public/faq.html', data)
