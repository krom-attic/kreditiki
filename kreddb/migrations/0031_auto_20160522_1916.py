# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-22 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0030_auto_20160522_1915'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BodyA',
            new_name='Body',
        ),
        migrations.RenameModel(
            old_name='CarModelA',
            new_name='CarModel',
        ),
        migrations.RenameModel(
            old_name='EngineA',
            new_name='Engine',
        ),
        migrations.RenameModel(
            old_name='GearA',
            new_name='Gear',
        ),
        migrations.RenameModel(
            old_name='GenerationA',
            new_name='Generation',
        ),
        migrations.RenameModel(
            old_name='ModificationA',
            new_name='Modification',
        ),
    ]
