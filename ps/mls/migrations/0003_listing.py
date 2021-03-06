# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-08 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0040_auto_20170108_0200'),
        ('mls', '0002_auto_20170108_1634'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mlsn', models.CharField(db_index=True, max_length=50, null=True)),
                ('pid', models.CharField(db_index=True, max_length=50, null=True)),
                ('status', models.CharField(db_index=True, max_length=10, null=True)),
                ('list_price', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sale_price', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('list_date', models.DateField(null=True)),
                ('sale_date', models.DateField(null=True)),
                ('dom', models.IntegerField(null=True)),
                ('type', models.CharField(max_length=50, null=True)),
                ('lot_size', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('style', models.CharField(max_length=50, null=True)),
                ('title', models.CharField(max_length=50, null=True)),
                ('year', models.IntegerField(null=True)),
                ('construction', models.CharField(max_length=50, null=True)),
                ('legal', models.CharField(max_length=250, null=True)),
                ('sqft', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sqft_a', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sqft_m', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sqft_e', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sqft_bu', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sqft_bf', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('sqft_b', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('development_units', models.IntegerField(null=True)),
                ('strata_units', models.IntegerField(null=True)),
                ('property', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='prop.Property')),
                ('source', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mls.Source')),
            ],
        ),
    ]
