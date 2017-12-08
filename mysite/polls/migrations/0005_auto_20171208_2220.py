# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-08 14:20
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0004_auto_20171123_1829'),
    ]

    operations = [
        migrations.AddField(
            model_name='giantmaintainmodel',
            name='more_info',
            field=models.CharField(default='##简要描述需要处理的单车问题##', max_length=9000, verbose_name='备注'),
        ),
        migrations.AddField(
            model_name='giantmaintainmodel',
            name='order_date',
            field=models.DateField(default=django.utils.timezone.now, help_text='填写预约的进行维保的日期', max_length=2000, verbose_name='预约日期'),
        ),
        migrations.AlterField(
            model_name='giantmaintainmodel',
            name='buy_date',
            field=models.DateField(default=django.utils.timezone.now, max_length=2000, verbose_name='购买日期'),
        ),
    ]
