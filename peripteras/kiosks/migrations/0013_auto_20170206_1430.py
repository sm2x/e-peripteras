# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0012_auto_20170202_1135'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kiosk',
            name='region',
            field=models.CharField(help_text='Region', max_length=60, null=True),
        ),
    ]
