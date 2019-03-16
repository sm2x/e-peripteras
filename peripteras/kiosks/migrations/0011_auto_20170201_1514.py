# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0010_auto_20170201_1314'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kiosk',
            name='address',
        ),
        migrations.AddField(
            model_name='kiosk',
            name='number',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='kiosk',
            name='street',
            field=models.CharField(help_text='Street', max_length=60, null=True),
        ),
        migrations.AddField(
            model_name='kiosk',
            name='tk',
            field=models.IntegerField(null=True),
        ),
    ]
