# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0020_auto_20170214_1521'),
    ]

    operations = [
        migrations.AddField(
            model_name='support',
            name='manager',
            field=models.ForeignKey(to='kiosks.KioskManager', null=True),
        ),
    ]
