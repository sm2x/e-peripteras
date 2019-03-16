# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_auto_20170131_1335'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stars', models.IntegerField()),
                ('text', models.TextField(default=b'', verbose_name='Feedback text', blank=True)),
                ('order', models.ForeignKey(to='users.Order')),
                ('simple_user', models.ForeignKey(to='users.SimpleUser')),
            ],
        ),
    ]
