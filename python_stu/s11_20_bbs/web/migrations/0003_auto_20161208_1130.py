# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20161208_1125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
