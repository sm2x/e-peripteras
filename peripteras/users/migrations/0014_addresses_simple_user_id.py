# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_order_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='addresses',
            name='simple_user_id',
            field=models.IntegerField(help_text='simple_user id', null=True),
        ),
    ]
