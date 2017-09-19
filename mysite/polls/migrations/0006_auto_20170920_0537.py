# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-19 21:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0005_auto_20170919_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='namemodel',
            name='assigned_to',
            field=models.CharField(default='', max_length=200, verbose_name='当前处理人'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='curent_state',
            field=models.CharField(max_length=200, verbose_name='当前状态'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='current_process',
            field=models.CharField(max_length=200, verbose_name='处理进展'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='deadline',
            field=models.CharField(max_length=200, verbose_name='截止时间'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='priority',
            field=models.CharField(max_length=200, verbose_name='重要性'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='processer_1st',
            field=models.CharField(default='', max_length=200, verbose_name='第一环节处理人'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='processer_2nd',
            field=models.CharField(default='', max_length=200, verbose_name='第二环节处理人'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='processer_3rd',
            field=models.CharField(default='', max_length=200, verbose_name='第三环节处理人'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='summary',
            field=models.CharField(max_length=200, verbose_name='概要'),
        ),
        migrations.AlterField(
            model_name='namemodel',
            name='urgency',
            field=models.CharField(max_length=200, verbose_name='紧急性'),
        ),
    ]
