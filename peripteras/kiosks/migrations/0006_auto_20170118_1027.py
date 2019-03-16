# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0005_item_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='distance',
            field=models.IntegerField(default=1, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='kiosk',
            name='time',
            field=models.IntegerField(default=30, null=True, blank=True),
        ),
    ]
