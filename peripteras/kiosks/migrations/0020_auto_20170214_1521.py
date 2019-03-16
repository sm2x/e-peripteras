# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0019_support'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='support',
            name='manager',
        ),
        migrations.AddField(
            model_name='support',
            name='kiosk',
            field=models.ForeignKey(to='kiosks.Kiosk', null=True),
        ),
    ]
