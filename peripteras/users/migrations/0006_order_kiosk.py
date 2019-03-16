# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0008_kiosk_info'),
        ('users', '0005_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='kiosk',
            field=models.ForeignKey(to='kiosks.Kiosk', null=True),
        ),
    ]
