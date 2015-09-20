# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('kreddb', '0011_auto_20150916_2112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='generation',
            options={'ordering': ['-bottom_age']},
        ),
        migrations.RemoveField(
            model_name='modification',
            name='safename',
        ),
    ]
