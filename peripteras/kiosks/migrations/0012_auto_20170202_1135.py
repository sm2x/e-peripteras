# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0011_auto_20170201_1514'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kiosk',
            old_name='distance',
            new_name='max_distance',
        ),
    ]
