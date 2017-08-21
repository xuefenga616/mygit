# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20161208_1133'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='summary',
            field=models.CharField(default=datetime.datetime(2016, 12, 8, 16, 3, 43, 619943, tzinfo=utc), max_length=255),
            preserve_default=False,
        ),
    ]
