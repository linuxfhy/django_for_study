# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-21 01:14
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0008_auto_20170921_0833'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='namemodel',
            name='deadline',
        ),
        migrations.RemoveField(
            model_name='namemodel',
            name='processer_3rd',
        ),
        migrations.RemoveField(
            model_name='namemodel',
            name='urgency',
        ),
        migrations.AddField(
            model_name='namemodel',
            name='detail',
            field=models.CharField(default=datetime.datetime(2017, 9, 21, 1, 13, 58, 891325, tzinfo=utc), max_length=200, verbose_name='详细描述'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='namemodel',
            name='value',
            field=models.CharField(default='', max_length=200, verbose_name='改进价值评估'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='priority',
            field=models.CharField(max_length=200, verbose_name='优先级'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='processer_2nd',
            field=models.CharField(default='', max_length=200, verbose_name='建议评审人'),
        ),
    ]