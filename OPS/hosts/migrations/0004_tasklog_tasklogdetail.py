# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0003_auto_20160808_2202'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('task_type', models.CharField(max_length=50, choices=[(b'multi_cmd', b'CMD'), (b'file_send', b'\xe6\x89\xb9\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe6\x89\xb9\xe9\x87\x8f\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')])),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(max_length=100, null=True, blank=True)),
                ('hosts', models.ManyToManyField(to='hosts.BindHostToUser')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u6279\u91cf\u4efb\u52a1',
                'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1',
            },
        ),
        migrations.CreateModel(
            name='TaskLogDetail',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('event_log', models.TextField()),
                ('result', models.CharField(default=b'unknown', max_length=30, choices=[(b'success', b'Success'), (b'failed', b'Failed'), (b'unknown', b'Unknown')])),
                ('note', models.CharField(max_length=100, blank=True)),
                ('bind_host', models.ForeignKey(to='hosts.BindHostToUser')),
                ('child_of_task', models.ForeignKey(to='hosts.TaskLog')),
            ],
            options={
                'verbose_name': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
                'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
            },
        ),
    ]
