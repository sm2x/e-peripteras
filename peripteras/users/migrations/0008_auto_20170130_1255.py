# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_auto_20170130_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='closed_on',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
