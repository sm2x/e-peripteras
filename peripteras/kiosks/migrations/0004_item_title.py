# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0003_brand_category_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='title',
            field=models.CharField(default=b'', max_length=255, verbose_name='Item title'),
        ),
    ]
