# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 05:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0015_auto_20161115_2114'),
    ]

    operations = [
        migrations.AddField(
            model_name='imp_tie',
            name='grp',
            field=models.BigIntegerField(null=True),
        ),
    ]
