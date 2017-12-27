# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-12-27 03:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0006_ess_ordersupportmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='ESS_CustomerIssueModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200, verbose_name='项目')),
                ('content', models.CharField(max_length=5000, verbose_name='主要工作内容')),
                ('customer', models.CharField(max_length=200, verbose_name='客户名称')),
                ('order_number', models.CharField(default='0', max_length=200, verbose_name='订单数量')),
                ('software_ver', models.CharField(default='0', max_length=200, verbose_name='软件版本')),
                ('responser', models.CharField(default='0', max_length=200, verbose_name='负责人')),
                ('responser_to_maitain', models.CharField(default='0', max_length=200, verbose_name='转维负责人')),
                ('deadline', models.CharField(default='0', max_length=200, verbose_name='完成日期')),
                ('current_process', models.CharField(default='##由改进实施人填写##', max_length=5000, verbose_name='当前进展')),
                ('assigned_to', models.CharField(default='', max_length=200, verbose_name='当前处理人(只读)')),
                ('created_by', models.CharField(default='', max_length=200, verbose_name='创建人(只读)')),
                ('curent_state', models.CharField(max_length=200, verbose_name='当前状态(只读)')),
            ],
        ),
    ]
