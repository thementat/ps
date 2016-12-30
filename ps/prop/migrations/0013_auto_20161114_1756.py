# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-14 17:56
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0012_parcel_ident'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('muni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Muni')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel_Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Lot')),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel')),
            ],
        ),
        migrations.RemoveField(
            model_name='parcel_ident',
            name='parcel',
        ),
        migrations.DeleteModel(
            name='Parcel_Ident',
        ),
    ]