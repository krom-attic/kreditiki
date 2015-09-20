# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0012_auto_20150916_2117'),
    ]

    operations = [
        migrations.AddField(
            model_name='generation',
            name='safe_name',
            field=models.CharField(db_index=True, blank=True, max_length=100),
        ),
    ]
