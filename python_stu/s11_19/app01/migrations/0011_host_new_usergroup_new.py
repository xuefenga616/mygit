# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0010_simplemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Host_new',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(max_length=64)),
                ('ip', models.GenericIPAddressField()),
                ('user_group', models.ForeignKey(to='app01.UserGroup')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup_new',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=64)),
                ('user_info', models.ManyToManyField(to='app01.UserInfo')),
            ],
        ),
    ]
