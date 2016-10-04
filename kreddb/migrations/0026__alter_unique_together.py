# -*- coding: utf-8 -*-
# Generated by Django 1.10.1 on 2016-09-26 21:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0025_auto_20160920_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='carmodel',
            name='name',
            field=models.CharField(default='', max_length=127),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='carmodel',
            unique_together=set([('model_family', 'name', 'generation', 'body')]),
        ),
    ]