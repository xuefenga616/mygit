# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0005_auto_20161208_0804'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=16)),
            ],
        ),
        migrations.CreateModel(
            name='Somthing',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('c1', models.CharField(max_length=10)),
                ('c2', models.CharField(max_length=10)),
                ('c3', models.CharField(max_length=10)),
                ('c4', models.CharField(max_length=10)),
                ('color', models.ForeignKey(to='app01.Color')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='name',
            field=models.CharField(max_length=32, unique=True, serialize=False, verbose_name='\u59d3\u540d', primary_key=True),
        ),
    ]
