# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BodyDB',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'body',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Body',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('kreddb.bodydb',),
        ),
    ]
