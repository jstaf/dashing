# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-09 02:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('slurm', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='nodes',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='start_time',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='time_limit',
            field=models.IntegerField(null=True),
        ),
    ]
