# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0009_aadmin'),
    ]

    operations = [
        migrations.CreateModel(
            name='SimpleModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
            ],
        ),
    ]
