# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20170130_1257'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='total_sum',
            field=models.DecimalField(null=True, max_digits=6, decimal_places=2),
        ),
    ]
