# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0005_article_summary'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(related_name='my_friends', to='web.UserProfile'),
        ),
    ]
