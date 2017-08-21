# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='email',
            field=models.EmailField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='email2',
            field=models.EmailField(default=b'123@qq.com', max_length=32),
        ),
    ]
