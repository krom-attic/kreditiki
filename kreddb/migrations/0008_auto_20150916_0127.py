# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0007_auto_20150916_0116'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Body',
        ),
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=253, unique=True)),
            ],
            options={
                'db_table': 'body',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='BodyCustom',
            fields=[
                ('body_ptr', models.OneToOneField(to='kreddb.Body', primary_key=True, parent_link=True, auto_created=True, serialize=False)),
                ('safename', models.CharField(blank=True, db_index=True, max_length=100)),
            ],
            bases=('kreddb.body',),
        ),
    ]
