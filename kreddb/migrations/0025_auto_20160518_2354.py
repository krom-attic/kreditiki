# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-18 20:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0024_auto_20160516_0041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='equipment',
            name='name',
            field=models.CharField(db_index=True, max_length=255),
        ),
    ]
