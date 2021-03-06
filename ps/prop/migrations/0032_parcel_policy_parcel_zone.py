# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-21 23:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0031_auto_20161121_2317'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel_Policy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel')),
                ('policy', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Policy')),
            ],
        ),
        migrations.CreateModel(
            name='Parcel_Zone',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
                ('parcel', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel')),
                ('zone', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Zone')),
            ],
        ),
    ]
