# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0006_auto_20150916_0100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enginecustom',
            old_name='safe_name',
            new_name='safename',
        ),
    ]
