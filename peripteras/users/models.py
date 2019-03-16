#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import uuid

from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from peripteras.kiosks.models import KioskManager


class SimpleUser(models.Model):
    """
    Definition of SimpleUser Model. This model extends the default
    Django User model with one to one field
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    first_name = models.CharField(max_length=60, blank=True, null=True,
                                  help_text=_(u'First name'))

    last_name = models.CharField(max_length=60, blank=True, null=True,
                                 help_text=_(u'Last name'))

    mobile_number = models.CharField(
        max_length=40, blank=True, null=True,
        verbose_name=_(u'Mobile Number'),
        validators=[
            RegexValidator(regex=r'("")|(^[0-9+]+$)',
                           message='Please only numbers and "+".')])

    addresses = models.ForeignKey('users.Addresses', blank=True, null=True)

    orders = models.ManyToManyField('users.Order', related_name='orders', blank=True, null=True)

    # avatar = ImageField(default='', blank=True, upload_to=_get_upload_path)

    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "Simple UserID: {0}".format(self.id)

    def get_full_name(self):
        return _(u'{0} {1}'.format(self.first_name, self.last_name))


class Addresses(models.Model):

    street = models.CharField(max_length=60, blank=False, null=True,
                              help_text=_(u'Street'))

    number = models.IntegerField()

    city = models.CharField(max_length=60, blank=False, null=True,
                            help_text=_(u'City'))

    region = models.CharField(max_length=60, blank=False, null=True,
                              help_text=_(u'Region'))

    tk = models.IntegerField()

    simple_user_id = models.IntegerField(blank=False, null=True,
                                         help_text=_(u'simple_user id'))

    class Meta:
        verbose_name_plural = "Addresses"

    def __unicode__(self):
        # return self.street + " " + str(self.number)
        # return "{0} {1} ({2}), {3}".format(self.street, self.number,
        # self.region, self.city)
        return "Address id: {0}".format(self.id)


class Order(models.Model):

    simple_user = models.ForeignKey(
        'users.SimpleUser', blank=False, null=False)

    first_name = models.CharField(max_length=60, blank=True, null=True,
                                  help_text=_(u'First name'))

    last_name = models.CharField(max_length=60, blank=True, null=True,
                                 help_text=_(u'Last name'))

    mobile_number = models.CharField(
        max_length=40, blank=True, null=True,
        verbose_name=_(u'Mobile Number'),
        validators=[
            RegexValidator(regex=r'("")|(^[0-9+]+$)',
                           message='Please only numbers and "+".')])

    address = models.ForeignKey('users.Addresses', blank=False, null=False)

    basket_items = models.ManyToManyField(
        'kiosks.Item', related_name='items', blank=True)
    # ord.basket_items.all()
    # ord.basket_items.add(itm)

    basket_items_ids = models.TextField(null=True)

    completed = models.NullBooleanField(
        default=False, blank=True, verbose_name=_(u'Completed order'))

    created_on = models.DateTimeField(auto_now_add=True)

    closed_on = models.DateTimeField(blank=True, null=True)

    kiosk = models.ForeignKey('kiosks.Kiosk', blank=False, null=True)

    total_sum = models.DecimalField(
        max_digits=6, decimal_places=2, blank=False, null=True)

    comments = models.TextField(default='', blank=True,
                                verbose_name=_(u'Comments'))

    def full_name(self):
        return _(u'{0} {1}'.format(self.first_name, self.last_name))

    def __unicode__(self):
        return "Order id: {0}".format(self.id)


def is_manager(self):
    try:
        manager = KioskManager.objects.get(user__id=self.id)
    except KioskManager.DoesNotExist:
        manager = False

    return manager

User.add_to_class("is_manager", is_manager)


class Feedback(models.Model):
    simple_user = models.ForeignKey(SimpleUser, null=False, blank=False)

    order = models.ForeignKey(Order, null=False, blank=False)

    stars = models.IntegerField()

    text = models.TextField(default='', blank=True,
                            verbose_name=_(u'Feedback text'))

    created_on = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        unique_together = ('simple_user', 'order',)

    def __unicode__(self):
        return u'Feedback id: {0}'.format(self.id)
