# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-18 20:44
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0023_auto_20161118_1904'),
    ]

    operations = [
        migrations.CreateModel(
            name='Imp_Lot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grp', models.CharField(db_index=True, max_length=50, null=True)),
                ('txt', models.CharField(db_index=True, max_length=50, null=True)),
                ('geom', django.contrib.gis.db.models.fields.MultiLineStringField(null=True, srid=4326)),
            ],
        ),
        migrations.AddField(
            model_name='lot',
            name='ext',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_address',
            name='txt',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='num',
            field=models.BigIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='num2',
            field=models.DecimalField(db_index=True, decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='num3',
            field=models.DecimalField(db_index=True, decimal_places=10, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='txt',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='txt2',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='txt3',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_property',
            name='txt',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_property',
            name='txt2',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_property',
            name='txt3',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_tie',
            name='grp',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_tie',
            name='txt',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_tie',
            name='txt2',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='imp_value',
            name='txt',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='ext',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='ext2',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='parcel_lot',
            name='grp',
            field=models.BigIntegerField(db_index=True, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='ext',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='property',
            name='ext2',
            field=models.CharField(db_index=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='imp_lot',
            name='lot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Lot'),
        ),
        migrations.AddField(
            model_name='imp_lot',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
    ]
