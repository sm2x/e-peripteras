# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_addresses_simple_user_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='simpleuser',
            name='orders',
            field=models.ManyToManyField(related_name='orders', to='users.Order'),
        ),
    ]
