# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import peripteras.kiosks.models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0009_kiosk_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kiosk',
            name='image',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=peripteras.kiosks.models._get_upload_path, blank=True),
        ),
    ]
