# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-10 04:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0009_auto_20161110_0036'),
    ]

    operations = [
        migrations.AddField(
            model_name='imp_parcel',
            name='postal',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='imp_property',
            name='postal',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='parcel',
            name='postal',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='property',
            name='postal',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
