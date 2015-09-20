# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0010_auto_20150916_2110'),
    ]

    operations = [
        migrations.AddField(
            model_name='modification',
            name='safename',
            field=models.CharField(db_index=True, max_length=100, blank=True),
        ),

    ]
