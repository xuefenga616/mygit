# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_auto_20161208_1130'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(default=datetime.datetime(2016, 12, 8, 11, 33, 55, 675846, tzinfo=utc), max_length=1000),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='parent_comment',
            field=models.ForeignKey(related_name='pComment', blank=True, to='web.Comment', null=True),
        ),
    ]
