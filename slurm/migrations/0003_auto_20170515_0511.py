# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-15 05:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('slurm', '0002_auto_20170509_0244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='command',
        ),
        migrations.RemoveField(
            model_name='node',
            name='tmp_disk',
        ),
    ]
