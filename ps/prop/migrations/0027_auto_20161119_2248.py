# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-19 22:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0026_auto_20161119_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imp_address',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_lot',
            name='lot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Lot'),
        ),
        migrations.AlterField(
            model_name='imp_lot',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_parcel',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_property',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_value',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Property'),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='lot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Lot'),
        ),
    ]
