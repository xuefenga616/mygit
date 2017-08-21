# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0006_auto_20161208_0959'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('nid', models.AutoField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Host',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=32)),
                ('business', models.ForeignKey(to='app01.Business')),
            ],
        ),
    ]
