# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_order_comments'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='first_name',
            field=models.CharField(help_text='First name', max_length=60, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='order',
            name='last_name',
            field=models.CharField(help_text='Last name', max_length=60, null=True, blank=True),
        ),
    ]
