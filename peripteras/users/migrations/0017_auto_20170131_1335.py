# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_order_basket_items_ids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='basket_items',
            field=models.ManyToManyField(related_name='items', to='kiosks.Item', blank=True),
        ),
    ]
