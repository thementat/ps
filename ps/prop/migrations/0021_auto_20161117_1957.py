# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 19:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0020_auto_20161116_2255'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imp',
            name='location',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='imp',
            name='source_type',
            field=models.CharField(max_length=20, null=True),
        ),
    ]