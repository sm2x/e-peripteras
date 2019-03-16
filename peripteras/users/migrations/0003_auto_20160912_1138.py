# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20160905_1555'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='addresses',
            options={'verbose_name_plural': 'Addresses'},
        ),
        migrations.AddField(
            model_name='simpleuser',
            name='first_name',
            field=models.CharField(help_text='First name', max_length=60, null=True, blank=True),
        ),
        migrations.AddField(
            model_name='simpleuser',
            name='last_name',
            field=models.CharField(help_text='Last name', max_length=60, null=True, blank=True),
        ),
    ]
