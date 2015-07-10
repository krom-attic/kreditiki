# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Body',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'body',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Email',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(unique=True, max_length=253)),
                ('verkey', models.CharField(null=True, max_length=253, blank=True)),
            ],
            options={
                'db_table': 'email',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'engine',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'equipment',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EquipmentDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
                ('cost', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'equipment_dict',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='EquipmentLk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'equipment_lk',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'feature',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FeatureDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'feature_dict',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='FeatureLk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'feature_lk',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Gear',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=253)),
            ],
            options={
                'db_table': 'gear',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Generation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
                ('cost', models.CharField(max_length=253)),
                ('age', models.CharField(max_length=253)),
                ('url', models.CharField(unique=True, max_length=253)),
                ('generation', models.CharField(null=True, max_length=253, blank=True)),
            ],
            options={
                'db_table': 'generation',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Mark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=253)),
                ('group_name', models.CharField(max_length=253)),
                ('url', models.CharField(max_length=253)),
                ('count', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'mark',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(unique=True, max_length=253)),
                ('generation_count', models.CharField(null=True, max_length=253, blank=True)),
                ('url', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'model',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Modification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
                ('url', models.CharField(unique=True, max_length=253)),
                ('complects_url', models.CharField(null=True, max_length=253, blank=True)),
                ('cost', models.CharField(null=True, max_length=253, blank=True)),
            ],
            options={
                'db_table': 'modification',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Trim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'trim',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrimDict',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=253)),
                ('value', models.CharField(max_length=253)),
            ],
            options={
                'db_table': 'trim_dict',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='TrimLk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'db_table': 'trim_lk',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ident', models.CharField(unique=True, max_length=253)),
                ('password', models.CharField(null=True, max_length=253, blank=True)),
            ],
            options={
                'db_table': 'user',
                'managed': False,
            },
        ),
    ]
