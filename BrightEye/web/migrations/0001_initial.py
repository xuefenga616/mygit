# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuditLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('action_type', models.IntegerField(default=0, choices=[(0, b'CMD'), (1, b'Login'), (2, b'Logout'), (3, b'GetFile'), (4, b'SendFile'), (5, b'exception')])),
                ('cmd', models.TextField()),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('date', models.DateTimeField()),
            ],
            options={
                'verbose_name': '\u5ba1\u8ba1\u65e5\u5fd7',
                'verbose_name_plural': '\u5ba1\u8ba1\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='BindHosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u4e0e\u8fdc\u7a0b\u7528\u6237\u7ed1\u5b9a',
                'verbose_name_plural': '\u4e3b\u673a\u4e0e\u8fdc\u7a0b\u7528\u6237\u7ed1\u5b9a',
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
            options={
                'verbose_name': '\u90e8\u95e8',
                'verbose_name_plural': '\u90e8\u95e8',
            },
        ),
        migrations.CreateModel(
            name='HostGroups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a\u7ec4',
                'verbose_name_plural': '\u4e3b\u673a\u7ec4',
            },
        ),
        migrations.CreateModel(
            name='Hosts',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('hostname', models.CharField(unique=True, max_length=64)),
                ('ip_addr', models.GenericIPAddressField(unique=True)),
                ('system_type', models.CharField(default=b'linux', max_length=32, choices=[(b'windows', b'Windows'), (b'linux', b'Linux')])),
                ('port', models.IntegerField(default=22)),
                ('enabled', models.BooleanField(default=True)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': '\u4e3b\u673a',
                'verbose_name_plural': '\u4e3b\u673a',
            },
        ),
        migrations.CreateModel(
            name='HostUsers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('auth_method', models.CharField(help_text='\u5982\u679c\u9009\u62e9SSH/KEY\uff0c\u8bf7\u786e\u4fdd\u79c1\u94a5\u6587\u4ef6\u5df2\u5728settings.py\u4e2d\u6307\u5b9a', max_length=16, choices=[(b'ssh-password', b'SSH/Password'), (b'ssh-key', b'SSH/KEY')])),
                ('username', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=64, null=True, blank=True)),
                ('memo', models.CharField(max_length=128, null=True, blank=True)),
            ],
            options={
                'verbose_name': '\u8fdc\u7a0b\u4e3b\u673a\u7528\u6237',
                'verbose_name_plural': '\u8fdc\u7a0b\u4e3b\u673a\u7528\u6237',
            },
        ),
        migrations.CreateModel(
            name='IDC',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='TaskLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('task_type', models.CharField(max_length=64, choices=[(b'cmd', b'CMD'), (b'file_send', '\u6279\u91cf\u53d1\u9001\u6587\u4ef6'), (b'file_get', '\u6279\u91cf\u4e0b\u8f7d\u6587\u4ef6')])),
                ('cmd', models.TextField()),
                ('task_pid', models.IntegerField(default=0)),
                ('note', models.CharField(max_length=128, null=True, blank=True)),
                ('hosts', models.ManyToManyField(to='web.BindHosts')),
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
                ('result', models.CharField(default=b'unknown', max_length=32, choices=[(b'success', b'Success'), (b'filed', b'Failed'), (b'unknown', b'Unknown')])),
                ('note', models.CharField(max_length=128, null=True, blank=True)),
                ('bind_host', models.ForeignKey(to='web.BindHosts')),
                ('child_of_task', models.ForeignKey(to='web.TaskLog')),
            ],
            options={
                'verbose_name': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
                'verbose_name_plural': '\u6279\u91cf\u4efb\u52a1\u65e5\u5fd7',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=32)),
                ('bind_hosts', models.ManyToManyField(to='web.BindHosts', verbose_name='\u6388\u6743\u4e3b\u673a', blank=True)),
                ('department', models.ForeignKey(verbose_name='\u90e8\u95e8', to='web.Department')),
                ('host_groups', models.ManyToManyField(to='web.HostGroups', verbose_name='\u6388\u6743\u4e3b\u673a\u7ec4', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'BrightEye\u8d26\u6237',
                'verbose_name_plural': 'BrightEye\u8d26\u6237',
            },
        ),
        migrations.AddField(
            model_name='tasklog',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='hostusers',
            unique_together=set([('auth_method', 'username', 'password')]),
        ),
        migrations.AddField(
            model_name='hosts',
            name='idc',
            field=models.ForeignKey(to='web.IDC'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host',
            field=models.ForeignKey(to='web.Hosts'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_group',
            field=models.ManyToManyField(to='web.HostGroups'),
        ),
        migrations.AddField(
            model_name='bindhosts',
            name='host_user',
            field=models.ForeignKey(to='web.HostUsers'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='host',
            field=models.ForeignKey(to='web.BindHosts'),
        ),
        migrations.AddField(
            model_name='auditlog',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AlterUniqueTogether(
            name='bindhosts',
            unique_together=set([('host', 'host_user')]),
        ),
    ]
