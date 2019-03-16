# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0017_auto_20170214_1307'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='activated',
            field=models.BooleanField(default=False, verbose_name='Activate kiosk or not'),
        ),
    ]
