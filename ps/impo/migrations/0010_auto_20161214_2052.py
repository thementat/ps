# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-14 20:52
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('impo', '0009_auto_20161212_1803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ilot',
            name='geom',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326),
        ),
    ]
