# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0025_kiosk_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kiosk',
            name='title',
            field=models.CharField(help_text='Kiosk title', max_length=60, null=True, blank=True),
        ),
    ]
