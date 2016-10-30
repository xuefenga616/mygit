# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('hosts', '0002_auto_20161015_1701'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('task_type', models.CharField(max_length=64, choices=[(b'multi_cmd', b'CMD'), (b'file_send', b'\xe6\x89\xb9\xe9\x87\x8f\xe5\x8f\x91\xe9\x80\x81\xe6\x96\x87\xe4\xbb\xb6'), (b'file_get', b'\xe6\x89\xb9\xe9\x87\x8f\xe4\xb8\x8b\xe8\xbd\xbd\xe6\x96\x87\xe4\xbb\xb6')])),
                ('cmd', models.TextField()),
                ('expire_time', models.IntegerField(default=30)),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(max_length=128, null=True, blank=True)),
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
                ('result', models.CharField(default=b'unknown', max_length=32, choices=[(b'success', b'Success'), (b'failed', b'Failed'), (b'unknown', b'Unknown')])),
                ('note', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'verbose_name': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
                'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
            },
        ),
        migrations.AlterModelOptions(
            name='bindhosttouser',
            options={'verbose_name': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a\u5173\u7cfb', 'verbose_name_plural': '\u4e3b\u673a\u4e0e\u7528\u6237\u7ed1\u5b9a\u5173\u7cfb'},
        ),
        migrations.AlterModelOptions(
            name='host',
            options={'verbose_name': '\u4e3b\u673a\u5217\u8868', 'verbose_name_plural': '\u4e3b\u673a\u5217\u8868'},
        ),
        migrations.AlterModelOptions(
            name='hostgroup',
            options={'verbose_name': '\u4e3b\u673a\u7ec4', 'verbose_name_plural': '\u4e3b\u673a\u7ec4'},
        ),
        migrations.AlterModelOptions(
            name='hostuser',
            options={'verbose_name': '\u8fdc\u7a0b\u4e3b\u673a\u7528\u6237', 'verbose_name_plural': '\u8fdc\u7a0b\u4e3b\u673a\u7528\u6237'},
        ),
        migrations.AddField(
            model_name='tasklogdetail',
            name='bind_host',
            field=models.ForeignKey(to='hosts.BindHostToUser'),
        ),
        migrations.AddField(
            model_name='tasklogdetail',
            name='child_of_task',
            field=models.ForeignKey(to='hosts.TaskLog'),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='hosts',
            field=models.ManyToManyField(to='hosts.BindHostToUser'),
        ),
        migrations.AddField(
            model_name='tasklog',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
