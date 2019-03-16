# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='kioskmanager',
            name='gender',
        ),
        migrations.AlterField(
            model_name='kioskmanager',
            name='kiosk',
            field=models.ForeignKey(blank=True, to='kiosks.Kiosk', null=True),
        ),
    ]
