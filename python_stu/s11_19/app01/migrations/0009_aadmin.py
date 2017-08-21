# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_auto_20161208_1027'),
    ]

    operations = [
        migrations.CreateModel(
            name='AAdmin',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('password', models.CharField(max_length=64)),
                ('user_info', models.OneToOneField(to='app01.User')),
            ],
        ),
    ]
