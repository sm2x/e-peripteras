# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0006_auto_20170118_1027'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='online_offer',
            field=models.NullBooleanField(default=False, verbose_name='Online offer'),
        ),
    ]
