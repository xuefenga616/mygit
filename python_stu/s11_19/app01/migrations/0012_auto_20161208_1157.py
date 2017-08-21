# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0011_host_new_usergroup_new'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usergroup_new',
            name='user_info',
        ),
        migrations.AlterField(
            model_name='host_new',
            name='user_group',
            field=models.ForeignKey(to='app01.UserGroup_new'),
        ),
    ]
