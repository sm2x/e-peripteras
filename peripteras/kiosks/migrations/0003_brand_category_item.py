# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kiosks', '0002_auto_20160905_1531'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='Brand name')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(default=b'', max_length=255, verbose_name='Category title')),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('slug', models.SlugField(unique=True, max_length=255, blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True, null=True)),
                ('brand', models.ForeignKey(to='kiosks.Brand')),
                ('category', models.ForeignKey(to='kiosks.Category')),
                ('kiosk', models.ForeignKey(to='kiosks.Kiosk')),
            ],
        ),
    ]
