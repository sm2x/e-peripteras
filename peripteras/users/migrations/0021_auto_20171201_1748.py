# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_feedback_created_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleuser',
            name='orders',
            field=models.ManyToManyField(related_name='orders', null=True, to='users.Order', blank=True),
        ),
    ]
