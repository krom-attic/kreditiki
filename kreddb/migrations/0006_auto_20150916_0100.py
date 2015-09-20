# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0005_auto_20150915_2223'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Engine',
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'engine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EngineCustom',
            fields=[
                ('engine_ptr', models.OneToOneField(serialize=False, auto_created=True, primary_key=True, to='kreddb.Engine', parent_link=True)),
                ('safe_name', models.CharField(db_index=True, blank=True, max_length=100)),
            ],
            bases=('kreddb.engine',),
        ),
    ]
