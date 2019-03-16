# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20160912_1138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simpleuser',
            name='addresses',
            field=models.ForeignKey(blank=True, to='users.Addresses', null=True),
        ),
    ]
