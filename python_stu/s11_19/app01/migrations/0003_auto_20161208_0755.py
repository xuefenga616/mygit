# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0002_auto_20161208_0738'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='img',
            field=models.ImageField(null=True, upload_to=b''),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='ip',
            field=models.GenericIPAddressField(null=True),
        ),
    ]
