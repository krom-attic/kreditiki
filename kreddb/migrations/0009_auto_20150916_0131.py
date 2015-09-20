# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0008_auto_20150916_0127'),
    ]

    operations = [
        migrations.RenameField(
            model_name='carmodelcustom',
            old_name='safe_name',
            new_name='safename',
        ),
        migrations.RenameField(
            model_name='markcustom',
            old_name='safe_name',
            new_name='safename',
        ),
    ]
