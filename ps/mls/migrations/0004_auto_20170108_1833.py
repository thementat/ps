# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-08 18:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mls', '0003_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='status',
            field=models.CharField(db_index=True, max_length=25, null=True),
        ),
        migrations.AlterField(
            model_name='search',
            name='name',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='source',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
