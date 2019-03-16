# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_feedback'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='feedback',
            unique_together=set([('simple_user', 'order')]),
        ),
    ]
