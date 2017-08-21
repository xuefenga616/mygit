# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20161208_0755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='img',
            field=models.ImageField(null=True, upload_to=b'upload'),
        ),
    ]
