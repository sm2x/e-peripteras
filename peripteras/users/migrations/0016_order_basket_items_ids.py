# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_simpleuser_orders'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='basket_items_ids',
            field=models.TextField(null=True),
        ),
    ]
