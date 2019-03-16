# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0024_auto_20170214_1729'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='is_open',
            field=models.BooleanField(default=True, verbose_name='Is kiosk open or not'),
        ),
    ]
