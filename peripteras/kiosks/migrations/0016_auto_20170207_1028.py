# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0015_auto_20170207_1026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='online_offer',
            field=models.NullBooleanField(default=False, verbose_name='Online offer'),
        ),
    ]
