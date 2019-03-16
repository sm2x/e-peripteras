# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import peripteras.kiosks.models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Kiosk',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(help_text='Address', max_length=60, null=True, blank=True)),
                ('city', models.CharField(help_text='City', max_length=60, null=True, blank=True)),
                ('region', models.CharField(help_text='Region', max_length=60, null=True, blank=True)),
                ('phone_number', models.CharField(blank=True, max_length=40, verbose_name='Phone Number', validators=[django.core.validators.RegexValidator(regex=b'("")|(^[0-9+]+$)', message=b'Please only numbers and "+".')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='KioskManager',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gender', models.NullBooleanField(default=None, verbose_name='Gender', choices=[(True, b'Female'), (False, b'Male')])),
                ('birth_date', models.DateField(help_text=b"Manager's birth date", null=True, validators=[peripteras.kiosks.models._validate_birth_date])),
                ('mobile_number', models.CharField(blank=True, max_length=40, verbose_name='Mobile Number', validators=[django.core.validators.RegexValidator(regex=b'("")|(^[0-9+]+$)', message=b'Please only numbers and "+".')])),
                ('email', models.EmailField(help_text=b"Kiosk Manager's contact emal.", max_length=254, null=True, blank=True)),
                ('kiosk', models.ForeignKey(to='kiosks.Kiosk', null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
