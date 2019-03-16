# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0014_remove_kiosk_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='online_offer',
            field=models.BooleanField(default=False),
        ),
    ]
