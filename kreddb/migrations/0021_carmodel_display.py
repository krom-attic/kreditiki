# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-18 10:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0020_auto_20160918_1213'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='display',
            field=models.BooleanField(default=False),
        ),
    ]