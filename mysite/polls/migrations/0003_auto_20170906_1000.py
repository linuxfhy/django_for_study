# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-06 02:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_namemodel'),
    ]

    operations = [
        migrations.RenameField(
            model_name='namemodel',
            old_name='summary',
            new_name='summary1',
        ),
    ]
