# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0008_kiosk_info'),
        ('users', '0004_auto_20160912_1210'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('completed', models.NullBooleanField(default=False, verbose_name='Completed order')),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('closed_on', models.DateTimeField()),
                ('address', models.ForeignKey(to='users.Addresses')),
                ('items', models.ManyToManyField(related_name='items', to='kiosks.Item')),
                ('simple_user', models.ForeignKey(to='users.SimpleUser')),
            ],
        ),
    ]
