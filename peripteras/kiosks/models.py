#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import uuid

from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django.contrib.auth.models import User
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from sorl.thumbnail import ImageField, get_thumbnail
from uuslug import uuslug as slugify

GENDER_CHOICES = (
    (True, 'Female'),
    (False, 'Male'),
)


def _validate_birth_date(data, **kwargs):
    """Validator to ensure age of at least 18 years old."""
    today = timezone.now().date()
    youth_threshold_day = (datetime.date(today.year - 18, today.month,
                                         today.day) +
                           datetime.timedelta(hours=24))
    if data > youth_threshold_day:
        raise ValidationError('Provided Birthdate is not valid.')
        return "N/A"

    return data


def _get_upload_path(instance, filename):
    return os.path.join(settings.ITEM_LOGO_DIR,
                        str(uuid.uuid4()) + '.jpg')


class KioskManager(models.Model):
    user = models.OneToOneField(User)

    kiosk = models.ForeignKey('kiosks.Kiosk', null=True, blank=True)

    birth_date = models.DateField(validators=[_validate_birth_date],
                                  blank=False, null=True,
                                  help_text="Manager's birth date")

    mobile_number = models.CharField(
        max_length=40, blank=True,
        verbose_name=_(u'Mobile Number'),
        validators=[
            RegexValidator(regex=r'("")|(^[0-9+]+$)',
                           message='Please only numbers and "+".')])

    email = models.EmailField(blank=True, null=True,
                              help_text="Kiosk Manager's contact emal.")

    def __unicode__(self):
        # return "Kiosk manager: id {0}".format(self.id)
        return u'Manager for: {0}'.format(self.kiosk)


class Kiosk(models.Model):

    title = models.CharField(max_length=60, blank=True, null=True,
                             help_text=_(u'Kiosk title'))

    street = models.CharField(max_length=60, blank=False, null=True,
                              help_text=_(u'Street'))

    number = models.IntegerField(null=True)

    region = models.CharField(max_length=60, blank=True, null=True,
                              help_text=_(u'Region'))

    tk = models.IntegerField(null=True)

    city = models.CharField(max_length=60, blank=True, null=True,
                            help_text=_(u'City'))

    activated = models.BooleanField(
        default=False, blank=True, verbose_name=_(u'Activate kiosk or not'))

    phone_number = models.CharField(
        max_length=40, blank=True,
        verbose_name=_(u'Phone Number'),
        validators=[
            RegexValidator(regex=r'("")|(^[0-9+]+$)',
                           message='Please only numbers and "+".')])

    info = models.CharField(max_length=400, blank=True, null=True,
                            help_text=_(u'Kiosk info'))

    max_distance = models.IntegerField(null=True, blank=True, default=1)

    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    image = ImageField(null=True, blank=True, upload_to=_get_upload_path)

    delivery_fee = models.DecimalField(
        max_digits=6, decimal_places=2, blank=False, default=0)

    is_open = models.BooleanField(
        default=True, blank=True, verbose_name=_(u'Is kiosk open or not'))

    def get_image_thumbnail(self, geometry=settings.AVATAR_DIMENSIONS, **kwargs):
        if 'crop' not in kwargs:
            kwargs['crop'] = 'center'
        if self.image:
            return get_thumbnail(self.image, geometry, **kwargs)
        return get_thumbnail(settings.DEFAULT_LOGO_PATH, geometry, **kwargs)

    def get_image_url(self, geometry=settings.KIOSK_DIMENSIONS, **kwargs):
        return self.get_image_thumbnail(geometry, **kwargs).url

    def __unicode__(self):
        # return '{0},{1},{2}'.format(self.street, self.number, self.city)
        return unicode('Kiosk id: {0}'.format(self.id))


class Item(models.Model):

    kiosk = models.ForeignKey('kiosks.Kiosk')

    price = models.DecimalField(max_digits=6, decimal_places=2, blank=False)

    brand = models.ForeignKey('kiosks.Brand', blank=False)

    title = models.CharField(max_length=255, default='', blank=False,
                                                     verbose_name=_(u'Item title'))

    slug = models.SlugField(unique=True, blank=True, max_length=255)

    category = models.ForeignKey('kiosks.Category')

    created_on = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True, null=True)

    image = ImageField(default='', blank=True, upload_to=_get_upload_path)

    online_offer = models.NullBooleanField(
        default=False, blank=False, verbose_name=_(u'Online offer'))

    # online_offer = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, instance=self)
        super(Item, self).save(*args, **kwargs)

    def is_offer(self):
        if self.online_offer:
            return (u'Ναι')
        return (u'Όχι')

    def get_item_name(self):
        return (u'{0}'.format(self.title))

    def __unicode__(self):
        return 'Item id: {0}'.format(self.id)


class Category(models.Model):
    title = models.CharField(max_length=255, default='', blank=False,
                                                     verbose_name=_(u'Category title'))

    slug = models.SlugField(unique=True, blank=True, max_length=255)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title, instance=self)
        super(Category, self).save(*args, **kwargs)

    def __unicode__(self):
        return (u'{0}'.format(self.title))

    class Meta:
        verbose_name_plural = "Categories"


class Brand(models.Model):
    title = models.CharField(max_length=255, default='', blank=False,
                                                     verbose_name=_(u'Brand name'))

    def __unicode__(self):
        return (u'{0}'.format(self.title))


class Support(models.Model):
    kiosk = models.ForeignKey('kiosks.Kiosk', null=True, blank=False)

    manager = models.ForeignKey('kiosks.KioskManager', null=True, blank=False)

    subject = models.CharField(max_length=100, default='', blank=False,
                               verbose_name=_(u'Subject'))

    text = models.TextField(default='', blank=True,
                            verbose_name=_(u'Comments'))

    def __unicode__(self):
        return unicode('{0}'.format(self.subject))
