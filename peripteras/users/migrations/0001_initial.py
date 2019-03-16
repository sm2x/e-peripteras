# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Addresses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(help_text='City', max_length=60, null=True)),
                ('region', models.CharField(help_text='Region', max_length=60, null=True)),
                ('street', models.CharField(help_text='Street', max_length=60, null=True)),
                ('number', models.IntegerField()),
                ('tk', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='SimpleUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mobile_number', models.CharField(blank=True, max_length=40, null=True, verbose_name='Mobile Number', validators=[django.core.validators.RegexValidator(regex=b'("")|(^[0-9+]+$)', message=b'Please only numbers and "+".')])),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('addresses', models.ForeignKey(to='users.Addresses')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
