# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0013_auto_20161208_1214'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_new',
            name='username',
            field=models.CharField(unique=True, max_length=64),
        ),
    ]
