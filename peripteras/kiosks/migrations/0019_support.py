# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0018_kiosk_activated'),
    ]

    operations = [
        migrations.CreateModel(
            name='Support',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subject', models.CharField(default=b'', max_length=100, verbose_name='Subject')),
                ('text', models.TextField(default=b'', verbose_name='Comments', blank=True)),
                ('manager', models.ForeignKey(to='kiosks.KioskManager', null=True)),
            ],
        ),
    ]
