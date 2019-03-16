#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import datetime
from django import forms
from django.forms.widgets import EmailInput, PasswordInput, TextInput, Select, NumberInput, DateInput

# from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from peripteras.users.models import SimpleUser, Feedback
from peripteras.kiosks.models import KioskManager, Kiosk


class LoginAuthenticationForm(AuthenticationForm):
    """Form for authenticating a requested user.

    Authenticates a user against the provided username
    and password.

    User can use as username his email or his actual username.
    """
    username = forms.CharField(required=True, max_length=50, widget=TextInput(attrs={
        'placeholder': 'Όνομα χρήστη', 'class': 'form-control input-lg', 'required': 'true'}))
    password = forms.CharField(required=True, widget=PasswordInput(attrs={
        'placeholder': 'Κωδικός', 'class': 'form-control input-lg', 'required': 'true'}))

    remember_me = forms.BooleanField(required=False, widget=forms.CheckboxInput())

    def clean_remember_me(self):
        if not self.cleaned_data.get('remember_me'):
            self.request.session.set_expiry(0)


class UserForm(forms.ModelForm):

    username = forms.CharField(required=True,
                               max_length=100,
                               error_messages={'unique': 'Το username είναι σε χρήση.',
                                               'required': 'Το πεδίο είναι υποχρεωτικό'},
                               widget=TextInput(attrs={
                                   'class': 'form-control input-md',
                                   'placeholder': "username",
                                   'required': 'True',
                                   'title': 'Πεδίο: Ψευώνυμο',

                               }))

    password = forms.CharField(required=True, widget=PasswordInput(attrs={
        'placeholder': 'Κωδικός',
        'required': 'true',
        'class': 'form-control input-md',
        'data-trigger': 'focus',
        'title': 'Πεδίο: Κωδικός',
        'data-content': 'Εισάγετε έναν κωδικό τον οποίο γνωρίζετε μόνο εσείς.'}))

    password2 = forms.CharField(required=True, widget=PasswordInput(attrs={
        'placeholder': 'Επαλήθευση κωδικού',
        'required': 'true',
        'class': 'form-control input-md',
        'data-trigger': 'focus',
        'title': 'Πεδίο: Επαλήθευση κωδικού',
        'data-content': 'Επαληθεύστε τον κωδικό.'}))

    email = forms.EmailField(error_messages={'invalid': 'Εισάγετε ένα έγκυρο email.'},
                             required=True,
                             widget=TextInput(attrs={
                                 'class': 'form-control input-md',
                                 'placeholder': "Email",
                                 'required': 'True',
                                 'data-trigger': 'focus',
                                 'title': 'Πεδίο: Email',
                                 'data-content': 'Εισάγετε ένα έγκυρο email.'
                             }))

    def clean_username(self):
        """Ensure data are valid."""
        data = self.cleaned_data['username']
        if not re.match(r'(^[\w.]+$)', data):
            raise forms.ValidationError(
                u'Επιτρέπονται γράμματα και αριθμοί χωρίς κενά.')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not re.match(r'(^[\D.]+$)', data, re.UNICODE):
            raise forms.ValidationError(u'Επιτρέπονται γράμματα χωρίς κενά.')
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if not re.match(r'(^[\D.]+$)', data, re.UNICODE):
            raise forms.ValidationError(u'Επιτρέπονται γράμματα χωρίς κενά.')
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(email=self.instance.email).exists():
            raise forms.ValidationError(u'Το email χρησιμοποιείται !')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError(u'Οι κωδικοί δεν ταιριάζουν.')
        return password

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')


class SimpleUserForm(forms.ModelForm):

    first_name = forms.CharField(required=True,
                                 max_length=100,
                                 widget=TextInput(attrs={
                                     'class': 'form-control input-md',
                                     'placeholder': "Όνομα",
                                     'required': 'True',
                                     'data-trigger': 'focus',
                                     'title': 'Πεδίο: Όνομα',
                                     'data-content': 'Εισάγετε το αληθινό όνομά σας.'

                                 }))

    last_name = forms.CharField(required=True,
                                max_length=100,
                                widget=TextInput(attrs={
                                    'class': 'form-control input-md',
                                    'placeholder': "Επίθετο",
                                    'required': 'True',
                                    'data-trigger': 'focus',
                                    'title': 'Πεδίο: Επίθετο',
                                    'data-content': 'Εισάγετε το αληθινό επίθετό σας.'

                                }))

    mobile_number = forms.IntegerField(error_messages={'invalid': 'Ο αριθμός πρέπει να έχει μορφη +301234567890.'},
                                       required=False,
                                       validators=[
        RegexValidator(
            regex=r'^\+?1?\d{9,15}$',
            message='Ο αριθμός πρέπει να έχει μορφη +301234567890',
            code='invalid'
        )
    ],
        widget=TextInput(
        attrs={'class': 'form-control input-md',
               'placeholder': 'Αριθμός',
               'data-toggle': 'popover',
               'data-trigger': 'focus',
               'title': 'Πεδίο: Αριθμός τηλεφώνου',
               'data-content': 'Ο αριμθός τηλεφώνου σας.'
               }))

    # address = forms.CharField(required=False,
    #                         max_length=100,
    #                         widget=TextInput(attrs={
    #                         'class': 'form-control input-sm',
    #                         'placeholder': "Διεύθυνση κατοικίας",
    #                         'data-trigger':'focus',
    #                         'title':'Πεδίο: Διεύθυνση',
    #                         'data-content':'Εισάγετε την διεύθυνσή σας.'}))

    class Meta:
        model = SimpleUser
        fields = ('first_name', 'last_name', 'mobile_number')



class UserManagerForm(forms.ModelForm):

    username = forms.CharField(required=True,
                               max_length=100,
                               error_messages={'unique': 'Το username είναι σε χρήση.',
                                               'required': 'Το πεδίο είναι υποχρεωτικό'},
                               widget=TextInput(attrs={
                                   'class': 'form-control input-md',
                                   'placeholder': "username",
                                   'required': 'True',
                                   'title': 'Πεδίο: Ψευώνυμο',

                               }))

    password = forms.CharField(required=True, widget=PasswordInput(attrs={
        'placeholder': 'Κωδικός',
        'required': 'true',
        'class': 'form-control input-md',
        'data-trigger': 'focus',
        'title': 'Πεδίο: Κωδικός',
        'data-content': 'Εισάγετε έναν κωδικό τον οποίο γνωρίζετε μόνο εσείς.'}))

    password2 = forms.CharField(required=True, widget=PasswordInput(attrs={
        'placeholder': 'Επαλήθευση κωδικού',
        'required': 'true',
        'class': 'form-control input-md',
        'data-trigger': 'focus',
        'title': 'Πεδίο: Επαλήθευση κωδικού',
        'data-content': 'Επαληθεύστε τον κωδικό.'}))

    email = forms.EmailField(error_messages={'invalid': 'Εισάγετε ένα έγκυρο email.'},
                             required=True,
                             widget=TextInput(attrs={
                                 'class': 'form-control input-md',
                                 'placeholder': "Email",
                                 'required': 'True',
                                 'data-trigger': 'focus',
                                 'title': 'Πεδίο: Email',
                                 'data-content': 'Εισάγετε ένα έγκυρο email.'
                             }))

    first_name = forms.CharField(required=True,
                                 max_length=100,
                                 widget=TextInput(attrs={
                                     'class': 'form-control input-ml',
                                     'placeholder': "Όνομα",
                                     'required': 'True',

                                 }))

    last_name = forms.CharField(required=True,
                                max_length=100,
                                widget=TextInput(attrs={
                                    'class': 'form-control input-ml',
                                    'placeholder': "Επίθετο",
                                    'required': 'True',

                                }))

    def clean_username(self):
        """Ensure data are valid."""
        data = self.cleaned_data['username']
        if not re.match(r'(^[\w.]+$)', data):
            raise forms.ValidationError(
                u'Επιτρέπονται γράμματα και αριθμοί χωρίς κενά.')
        return data

    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not re.match(r'(^[\D.]+$)', data, re.UNICODE):
            raise forms.ValidationError(u'Επιτρέπονται γράμματα χωρίς κενά.')
        return data

    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if not re.match(r'(^[\D.]+$)', data, re.UNICODE):
            raise forms.ValidationError(u'Επιτρέπονται γράμματα χωρίς κενά.')
        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(email=self.instance.email).exists():
            raise forms.ValidationError(u'Το email χρησιμοποιείται !')
        return email

    def clean_password2(self):
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError(u'Οι κωδικοί δεν ταιριάζουν.')
        return password

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2', 'first_name', 'last_name')


class ManagerForm(forms.ModelForm):

    class Meta:
        model = KioskManager
        fields = ('birth_date', 'mobile_number',)

class KioskForm(forms.ModelForm):

    class Meta:
        model = Kiosk
        fields = ('street', 'number', 'city','tk', 'title')


class FeedbackForm(forms.ModelForm):

    stars = forms.IntegerField(required=True, label=_(u'Αστέρια'),
                                widget=TextInput(
                                    attrs={'class': 'form-control input-md',
                                           'placeholder': 'Αστέρια',
                                           }))

    text = forms.CharField(required=False, label=_(u'Σχόλια'),
        widget=forms.Textarea(attrs={
        'class': 'form-control input-md',
        'rows': '5',
        'placeholder': 'Πείτε μας την γνώμη σας'}
    ))

    


    class Meta:
        model = Feedback
        fields = ('stars', 'text')
