# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-09 18:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0005_auto_20161109_1855'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imp_tie',
            name='num',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='imp_tie',
            name='txt',
            field=models.CharField(max_length=50, null=True),
        ),
    ]