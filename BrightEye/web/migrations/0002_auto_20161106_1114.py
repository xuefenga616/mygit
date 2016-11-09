# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.CharField(max_length=64)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire', models.IntegerField(default=300)),
                ('host', models.ForeignKey(to='web.BindHosts')),
                ('user', models.ForeignKey(to='web.UserProfile')),
            ],
        ),
        migrations.AddField(
            model_name='tasklog',
            name='expire_time',
            field=models.IntegerField(default=30),
        ),
    ]
