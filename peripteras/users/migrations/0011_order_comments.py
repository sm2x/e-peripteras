# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_order_total_sum'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='comments',
            field=models.TextField(default=b'', verbose_name='Comments', blank=True),
        ),
    ]
