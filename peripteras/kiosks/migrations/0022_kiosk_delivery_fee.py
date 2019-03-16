# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0021_support_manager'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='delivery_fee',
            field=models.DecimalField(default=0, max_digits=6, decimal_places=2),
        ),
    ]
