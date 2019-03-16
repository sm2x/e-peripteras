# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0007_item_online_offer'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='info',
            field=models.CharField(help_text='Kiosk info', max_length=400, null=True, blank=True),
        ),
    ]
