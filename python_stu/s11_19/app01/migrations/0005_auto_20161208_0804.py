# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_auto_20161208_0756'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='id',
        ),
        migrations.AddField(
            model_name='userinfo',
            name='user_type',
            field=models.IntegerField(default=1, choices=[(0, b'f'), (0, b'm')]),
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=32, serialize=False, primary_key=True),
        ),
    ]
