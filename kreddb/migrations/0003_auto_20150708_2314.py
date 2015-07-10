# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0002_body_bodydb'),
    ]

    operations = [
        migrations.CreateModel(
            name='EngineDB',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'engine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='GearDB',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'gear',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='MarkDB',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=253)),
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
            name='KredModification',
            fields=[
                ('modification_ptr', models.OneToOneField(to='kreddb.Modification', parent_link=True, serialize=False, primary_key=True, auto_created=True)),
                ('tie_braker', models.SmallIntegerField(blank=True, null=True)),
            ],
            bases=('kreddb.modification',),
        ),
        migrations.AlterModelOptions(
            name='generation',
            options={'managed': False, 'ordering': ['-bottom_age']},
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('kreddb.enginedb',),
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('kreddb.geardb',),
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
            ],
            options={
                'proxy': True,
            },
            bases=('kreddb.markdb',),
        ),
    ]
