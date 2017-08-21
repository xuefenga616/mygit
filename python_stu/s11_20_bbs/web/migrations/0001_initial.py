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
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(unique=True, max_length=255, verbose_name='\u6587\u7ae0\u6807\u9898')),
                ('head_img', models.ImageField(upload_to=b'uploads')),
                ('content', models.TextField()),
                ('publish_date', models.DateTimeField(auto_now=True)),
                ('hidden', models.BooleanField(default=True)),
                ('priority', models.IntegerField(default=1000, verbose_name='\u4f18\u5148\u7ea7')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.TextField(max_length=1000)),
                ('date', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(to='web.Article')),
                ('parent_comment', models.ForeignKey(related_name='pComment', to='web.Comment')),
            ],
        ),
        migrations.CreateModel(
            name='ThumbUp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(auto_now=True)),
                ('article', models.ForeignKey(to='web.Article')),
            ],
        ),
        migrations.CreateModel(
            name='UserGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=32)),
                ('groups', models.ManyToManyField(to='web.UserGroup')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='thumbup',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AddField(
            model_name='category',
            name='admin',
            field=models.ManyToManyField(to='web.UserProfile'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(to='web.UserProfile'),
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(verbose_name='\u7248\u5757', to='web.Category'),
        ),
    ]
