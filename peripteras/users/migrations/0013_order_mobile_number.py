# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_auto_20170131_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='mobile_number',
            field=models.CharField(blank=True, max_length=40, null=True, verbose_name='Mobile Number', validators=[django.core.validators.RegexValidator(regex=b'("")|(^[0-9+]+$)', message=b'Please only numbers and "+".')]),
        ),
    ]
