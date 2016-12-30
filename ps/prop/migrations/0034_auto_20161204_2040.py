# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-04 20:40
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0033_auto_20161121_2323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Parcel_Policybound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Parcel_Zonebound',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('area', models.DecimalField(decimal_places=4, max_digits=20, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='parcel_policy',
            name='parcel',
        ),
        migrations.RemoveField(
            model_name='parcel_policy',
            name='policy',
        ),
        migrations.RemoveField(
            model_name='parcel_zone',
            name='parcel',
        ),
        migrations.RemoveField(
            model_name='parcel_zone',
            name='zone',
        ),
        migrations.RemoveField(
            model_name='parcel',
            name='policy',
        ),
        migrations.RemoveField(
            model_name='parcel',
            name='zone',
        ),
        migrations.AddField(
            model_name='muni',
            name='srid',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Parcel_Policy',
        ),
        migrations.DeleteModel(
            name='Parcel_Zone',
        ),
        migrations.AddField(
            model_name='parcel_zonebound',
            name='parcel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
        migrations.AddField(
            model_name='parcel_zonebound',
            name='zonebound',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Zonebound'),
        ),
        migrations.AddField(
            model_name='parcel_policybound',
            name='parcel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
        migrations.AddField(
            model_name='parcel_policybound',
            name='policybound',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='prop.Policybound'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='policybound',
            field=models.ManyToManyField(blank=True, through='prop.Parcel_Policybound', to='prop.Policybound'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='zonebound',
            field=models.ManyToManyField(blank=True, through='prop.Parcel_Zonebound', to='prop.Zonebound'),
        ),
    ]
