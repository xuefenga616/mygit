# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0012_auto_20161208_1157'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_new',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('username', models.CharField(max_length=64)),
                ('user_group', models.ForeignKey(to='app01.UserGroup_new')),
            ],
        ),
        migrations.RemoveField(
            model_name='host_new',
            name='user_group',
        ),
        migrations.DeleteModel(
            name='Host_new',
        ),
    ]
