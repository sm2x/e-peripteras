# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleuser',
            name='addresses',
            field=models.ForeignKey(to='users.Addresses', blank=True),
        ),
    ]
