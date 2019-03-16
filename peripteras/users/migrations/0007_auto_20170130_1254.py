# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_order_kiosk'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='closed_on',
            field=models.DateTimeField(blank=True),
        ),
    ]
