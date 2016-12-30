# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-07 19:08
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prop', '0035_auto_20161207_0003'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('num', models.BigIntegerField(null=True)),
                ('unit', models.CharField(max_length=20, null=True)),
                ('street_number', models.IntegerField(null=True)),
                ('street_prefix', models.CharField(max_length=20, null=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('street_type', models.CharField(max_length=20, null=True)),
                ('street_suffix', models.CharField(max_length=20, null=True)),
                ('postal', models.CharField(max_length=20, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(null=True, srid=4326)),
                ('lot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Lot')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt2', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt3', models.CharField(db_index=True, max_length=50, null=True)),
                ('num', models.BigIntegerField(db_index=True, null=True)),
                ('num2', models.DecimalField(db_index=True, decimal_places=10, max_digits=20, null=True)),
                ('num3', models.DecimalField(db_index=True, decimal_places=10, max_digits=20, null=True)),
                ('unit', models.CharField(max_length=20, null=True)),
                ('street_number', models.IntegerField(null=True)),
                ('street_prefix', models.CharField(max_length=20, null=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('street_type', models.CharField(max_length=20, null=True)),
                ('street_suffix', models.CharField(max_length=20, null=True)),
                ('postal', models.CharField(max_length=20, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('parcel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Parcel')),
            ],
        ),
        migrations.CreateModel(
            name='Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=250, null=True)),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt2', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt3', models.CharField(db_index=True, max_length=50, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt2', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt3', models.CharField(db_index=True, max_length=50, null=True)),
                ('num', models.BigIntegerField(null=True)),
                ('num2', models.DecimalField(decimal_places=10, max_digits=20, null=True)),
                ('num3', models.DecimalField(decimal_places=10, max_digits=20, null=True)),
                ('unit', models.CharField(max_length=20, null=True)),
                ('street_number', models.IntegerField(null=True)),
                ('street_prefix', models.CharField(max_length=20, null=True)),
                ('street', models.CharField(max_length=50, null=True)),
                ('street_type', models.CharField(max_length=20, null=True)),
                ('street_suffix', models.CharField(max_length=20, null=True)),
                ('postal', models.CharField(max_length=20, null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('parcel', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impo.Parcel')),
            ],
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=50)),
                ('source_type', models.CharField(max_length=20, null=True)),
                ('location', models.CharField(max_length=250, null=True)),
                ('update_date', models.DateField(null=True)),
                ('muni', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Muni')),
            ],
        ),
        migrations.CreateModel(
            name='Source_Link',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_col', models.CharField(max_length=50)),
                ('model_col', models.CharField(max_length=50)),
                ('imp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='impo.Source')),
            ],
        ),
        migrations.CreateModel(
            name='Value',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valdate', models.CharField(max_length=50, null=True)),
                ('landval', models.IntegerField(null=True)),
                ('impval', models.IntegerField(null=True)),
                ('val', models.IntegerField(null=True)),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('num', models.BigIntegerField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impo.Property')),
            ],
        ),
        migrations.CreateModel(
            name='Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=20, null=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('url', models.CharField(max_length=250, null=True)),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt2', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt3', models.CharField(db_index=True, max_length=50, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(null=True, srid=4326)),
            ],
        ),
        migrations.AddField(
            model_name='lot',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impo.Parcel'),
        ),
        migrations.AddField(
            model_name='address',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='impo.Parcel'),
        ),
    ]
