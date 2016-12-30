# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 19:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0016_imp_tie_grp'),
    ]

    operations = [
        migrations.AddField(
            model_name='lot',
            name='agg',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parcel_lot',
            name='num',
            field=models.BigIntegerField(null=True),
        ),
    ]