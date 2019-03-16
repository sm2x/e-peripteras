# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0013_auto_20170206_1430'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kiosk',
            name='time',
        ),
    ]
