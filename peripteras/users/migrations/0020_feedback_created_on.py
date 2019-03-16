# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_auto_20170215_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
