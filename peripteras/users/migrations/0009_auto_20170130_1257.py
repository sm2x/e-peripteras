# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20170130_1255'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='items',
            new_name='basket_items',
        ),
    ]
