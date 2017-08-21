# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0007_business_host'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
                ('email', models.CharField(max_length=16)),
                ('mobile', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='user_user_group',
            field=models.ManyToManyField(to='app01.UserGroup'),
        ),
    ]
