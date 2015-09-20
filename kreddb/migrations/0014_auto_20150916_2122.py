# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0013_auto_20150916_2119'),
    ]

    operations = [
        migrations.RenameField(
            model_name='generation',
            old_name='safe_name',
            new_name='safename',
        ),
        migrations.AddField(
            model_name='modification',
            name='safename',
            field=models.CharField(blank=True, db_index=True, max_length=100),
        ),
    ]
