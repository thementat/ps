# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-11 04:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0036_auto_20161208_1825'),
    ]

    operations = [
        migrations.AlterField(
            model_name='value',
            name='impval',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='value',
            name='landval',
            field=models.BigIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='value',
            name='val',
            field=models.BigIntegerField(null=True),
        ),
    ]
