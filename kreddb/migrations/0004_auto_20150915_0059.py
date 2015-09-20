# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0003_auto_20150708_2314'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModelCustom',
            fields=[
                ('model_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, serialize=False, to='kreddb.Model')),
                ('safe_name', models.CharField(max_length=100, blank=True)),
            ],
            bases=('kreddb.model',),
        ),
        migrations.DeleteModel(
            name='Mark',
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=253, unique=True)),
                ('group_name', models.CharField(max_length=253)),
                ('url', models.CharField(max_length=253)),
                ('count', models.IntegerField()),
            ],
            options={
                'db_table': 'mark',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MarkCustom',
            fields=[
                ('mark_ptr', models.OneToOneField(primary_key=True, parent_link=True, auto_created=True, serialize=False, to='kreddb.Mark')),
                ('safe_name', models.CharField(max_length=100, blank=True)),
            ],
            options={
                'managed': True,
            },
            bases=('kreddb.mark',),
        ),
    ]
