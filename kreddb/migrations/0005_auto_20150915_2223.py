# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0004_auto_20150915_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(unique=True, max_length=253)),
                ('generation_count', models.CharField(max_length=253, blank=True)),
                ('url', models.CharField(max_length=253)),
                ('bottom_age', models.IntegerField(null=True, blank=True)),
                ('top_age', models.IntegerField(null=True, blank=True)),
            ],
            options={
                'db_table': 'model',
                'managed': False,
            },
        ),
        migrations.RemoveField(
            model_name='carmodelcustom',
            name='model_ptr',
        ),
        migrations.AlterField(
            model_name='carmodelcustom',
            name='safe_name',
            field=models.CharField(db_index=True, max_length=100, blank=True),
        ),
        migrations.AddField(
            model_name='carmodelcustom',
            name='carmodel_ptr',
            field=models.OneToOneField(auto_created=True, serialize=False, to='kreddb.CarModel', primary_key=True, parent_link=True, default=None),
            preserve_default=False,
        ),
    ]
