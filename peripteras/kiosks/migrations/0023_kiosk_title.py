# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0022_kiosk_delivery_fee'),
    ]

    operations = [
        migrations.AddField(
            model_name='kiosk',
            name='title',
            field=models.CharField(help_text='Street', max_length=60, null=True),
        ),
    ]
