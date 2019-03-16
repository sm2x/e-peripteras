#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import datetime
import csv
import xlrd

from django import forms
from django.conf import settings
from django.forms.widgets import EmailInput, PasswordInput, TextInput, Select, NumberInput, DateInput

# from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from peripteras.kiosks.models import KioskManager, Kiosk, Item, Brand, Category, Support


class KioskForm(forms.ModelForm):

    IS_OPEN = (
        (True, 'Ναι'),
        (False, 'Όχι'),
    )

    title = forms.CharField(required=True, label=_(u'Επωνυμία'),
                            max_length=100,
                            widget=TextInput(attrs={
                                'class': 'form-control input-md',
                                'placeholder': "Επωνυμία επιχείρησης",
                                'required': 'True'

                            }))
    street = forms.CharField(required=True, label=_(u'Οδός'),
                             max_length=100,
                             widget=TextInput(attrs={
                                 'class': 'form-control input-md',
                                 'placeholder': "Διεύθυνση",
                                 'required': 'True',

                             }))

    number = forms.IntegerField(required=True, label=_(u'Αριθμός'),
                                widget=TextInput(
                                    attrs={'class': 'form-control input-md',
                                           'placeholder': 'Αριθμός',
                                           'required': 'True'
                                           }))

    city = forms.CharField(required=True, label=_(u'Πόλη'),
                           max_length=100,
                           widget=TextInput(attrs={
                               'class': 'form-control input-md',
                               'placeholder': "Πόλη",
                               'required': 'True'

                           }))

    delivery_fee = forms.DecimalField(required=True, label=_(u'Έξτρα χρέωση μεταφοράς σε €'),
                                      widget=TextInput(
                                          attrs={'class': 'form-control input-md',
                                                 'placeholder': 'πχ. 3€',
                                                 'required': 'True'
                                                 }))

    tk = forms.IntegerField(required=True, label=_(u'Ταχ.Κώδικας'),
                            widget=TextInput(
                                attrs={'class': 'form-control input-md',
                                       'placeholder': 'TK',
                                       'required': 'True'
                                       }))

    region = forms.CharField(required=True, label=_(u'Περιοχή'),
                             max_length=100,
                             widget=TextInput(attrs={
                                 'class': 'form-control input-md',
                                 'placeholder': "Περιοχή",
                                 'required': 'True',

                             }))

    phone_number = forms.IntegerField(label=_(u'Τηλ. Επικοινωνίας'),
                                      error_messages={
                                          'invalid': 'Ο αριθμός πρέπει να έχει μορφη +301234567890.'},
                                      required=True,
                                      validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Ο αριθμός πρέπει να έχει μορφη +301234567890',
            code='invalid'
        )
    ],
        widget=TextInput(
        attrs={'class': 'form-control input-md',
               'placeholder': 'Αριθμός τηλεφώνου',
               'required': 'True'
               }))

    max_distance = forms.IntegerField(required=True, label=_(u'Μέγιστη απόσταση που εξυπηρετείτε σε χιλιόμετρα'),
                                      widget=TextInput(
                                          attrs={'class': 'form-control input-md',
                                                 'placeholder': 'Απόσταση σε χιλιόμετρα',
                                                 'required': 'True'
                                                 }))

    info = forms.CharField(required=False, label=_(u'Πληροφορίες'),
                           widget=forms.Textarea(attrs={
                               'class': 'form-control input-md',
                               'rows': '3',
                               'placeholder': 'Μερικές πληροφορίες/σχόλια'}
    ))

    is_open = forms.ChoiceField(label=_(u'Εϊστε ανοιχτά'), choices=IS_OPEN, required=True,
                                widget=forms.Select(attrs={
                                    'class': 'form-control input-md',
                                    'required': 'True',

                                }))

    class Meta:
        model = Kiosk
        fields = '__all__'
        exclude = ('activated',)


class ItemForm(forms.ModelForm):

    ONLINE_OFFER = (
        ('True', 'Ναι'),
        ('False', 'Όχι'),
    )

    title = forms.CharField(required=True,
                            max_length=100,
                            widget=TextInput(attrs={
                                'class': 'form-control input-md',
                                'placeholder': "Τίτλος",
                                'required': 'True',

                            }))

    price = forms.DecimalField(error_messages={'invalid': 'Επιτρέπονται μόνο αριθμοί.',
                                               'required': 'Η τιμή είναι υποχρεωτικό πεδίο'},
                               max_digits=7, decimal_places=2,
                               required=True,
                               widget=TextInput(attrs={
                                   'class': 'form-control input-md',
                                   'placeholder': "Τιμή σε €",
                                   'required': 'True',
                               }))

    brand = forms.ModelChoiceField(queryset=Brand.objects.all(),
                                   empty_label='Επιλέξτε Μάρκα',
                                   required=True,
                                   widget=Select(
        attrs={
            'class': 'form-control input-md',
        }))

    category = forms.ModelChoiceField(queryset=Category.objects.all(),
                                      empty_label='Επιλέξτε κατηγορία',
                                      required=True,
                                      widget=Select(
        attrs={
            'class': 'form-control input-md',
        }))

    online_offer = forms.ChoiceField(choices=ONLINE_OFFER, required=True,
                                     widget=forms.Select())

    def clean_brand(self):
        """Ensure that brand is valid."""
        data = self.cleaned_data['brand']
        try:
            brand = Brand.objects.get(title=data)
            return brand
        except Brand.DoesNotExist:
            raise forms.ValidationError(u'Σφάλμα στην επιλογή μάρκας')

    class Meta:
        model = Item
        fields = '__all__'
        exclude = ('kiosk', 'slug')


class SupportForm(forms.ModelForm):

    subject = forms.CharField(required=True,
                              max_length=100,
                              widget=TextInput(attrs={
                                  'class': 'form-control input-md',
                                  'placeholder': "Θέμα",
                                  'required': 'True',

                              }))

    text = forms.CharField(required=False, widget=forms.Textarea(attrs={
        'class': 'form-control input-md',
        'rows': '5',
        'placeholder': "Περιγράψτε το πρόβλημά σας...", }
    ))

    class Meta:
        model = Support
        fields = ('subject', 'text')


class CSVMixin(object):
    """Generic Mixin that defines a clean method
    fo a csv file.
    """

    def clean_uploaded_file(self):
        """Validates and returns an uploaded csv file."""
        input_type = self.cleaned_data['input_type']
        data = self.cleaned_data['uploaded_file']
        required_headers = [header_name for header_name, values
                            in self.HEADERS.items() if values['required']]
        print 'required_headers: %s' % required_headers
        if input_type == 'csv':
            # first check the content type
            if data.content_type in settings.EXCEL_FORMATS:
                raise ValidationError(u'Not a valid csv file')
            # check file valid csv format
            try:
                dialect = csv.Sniffer().sniff(data.read(1024), delimiters=',')
                data.seek(0)
            except csv.Error:
                print csv.Error.message
                raise ValidationError(u'Not a valid csv file!')

            print 'Valid csv file: %s' % dialect
            print 'delimiters %s:' % dialect.delimiter
            reader = csv.reader(data.read().splitlines(), dialect)

            for y_index, row in enumerate(reader):
                # check that all headers are present
                if y_index == 0:
                    # store header names to sanity check required cells later
                    csv_headers = [header_name.lower() for header_name
                                   in row if header_name]
                    missing_headers = set(
                        required_headers) - set([r.lower() for r in row])
                    if missing_headers:
                        missing_headers_str = ', '.join(missing_headers)
                        raise ValidationError(
                            u'Missing headers: %s' % missing_headers_str)
                    continue

                # ignore blank rows
                if not ''.join(str(x) for x in row):
                    continue

                for x_index, cell_value in enumerate(row):
                    try:
                        csv_headers[x_index]
                    except IndexError:
                        continue

                    # if csv_headers[x_index] in required_headers:
                    #     if not cell_value:
                    #         raise ValidationError(u'Missing required value %s for row %s' %
                    #                               (csv_headers[x_index], y_index + 1))
        else:
            # first check content type
            if data.content_type in settings.CSV_FORMATS:
                raise ValidationError(u'Not a valid excel file')
            try:
                book = xlrd.open_workbook(data.name, file_contents=data.read())
                data.seek(0, 0)
            except xlrd.XLRDError:
                raise ValidationError(u'Not a valid excel file')

            cnt = 0
            sheets = book.sheets()
            for sheet in sheets:
                # sheet = book.sheet_by_name('Sheet1')
                # read header values into the list
                keys = [sheet.cell(0, col_index).value.strip()
                        for col_index in xrange(sheet.ncols)]
                if not keys:
                    cnt += 1
                    continue

                missing_headers = set(required_headers) - set(keys)
                if missing_headers:
                    missing_headers_str = ', '.join(missing_headers)
                    raise ValidationError(
                        u'Missing headers: %s' % missing_headers_str)

            if cnt == len(sheets):
                raise ValidationError(u'No headers found at all')

        return data


class CSVImportForm(CSVMixin, forms.Form):
    """Form to upload a csv file. """
    HEADERS = {
        'price': {'field': 'price', 'required': True},
        'brand': {'field': 'brand', 'required': True},
        'title': {'field': 'title', 'required': True},
        'category': {'field': 'category', 'required': True},
    }

    CHOICES = (
        ('csv', 'csv file'),
    )

    input_type = forms.ChoiceField(label='Select available type', choices=CHOICES, required=True,
                                   widget=forms.RadioSelect(attrs={'required': 'true'}))
    uploaded_file = forms.FileField(label='Find the list')
    kiosk = forms.ModelChoiceField(queryset=None,
                                   label='Select your Kiosk',
                                   required=True,
                                   widget=Select(
                                       attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        """Uses keyword ``managerid`` to ensure that displayed
        department choices will be only related to requested
        manager.
        """
        kiosk = kwargs.pop('kiosk', None)
        super(CSVImportForm, self).__init__(*args, **kwargs)
        if not kiosk:
            raise Exception('No kiosk was related')
        self.fields['kiosk'].queryset = kiosk.all()
