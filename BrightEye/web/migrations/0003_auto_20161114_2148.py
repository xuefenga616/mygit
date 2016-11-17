# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0002_auto_20161106_1114'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasklog',
            name='task_type',
            field=models.CharField(max_length=64, choices=[(b'cmd', b'CMD'), (b'file_send', '\u6279\u91cf\u53d1\u9001\u6587\u4ef6'), (b'file_get', '\u6279\u91cf\u4e0b\u8f7d\u6587\u4ef6'), (b'bigtask', '\u8ba1\u5212\u4efb\u52a1')]),
        ),
    ]
