# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-16 22:55
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0019_auto_20161116_2138'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='src',
            name='muni',
        ),
        migrations.RemoveField(
            model_name='src_imp',
            name='imp',
        ),
        migrations.RemoveField(
            model_name='src_imp',
            name='src',
        ),
        migrations.AddField(
            model_name='imp_parcel',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
        migrations.AddField(
            model_name='imp_tie',
            name='lot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Lot'),
        ),
        migrations.AddField(
            model_name='imp_tie',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_address',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_property',
            name='parcel',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Parcel'),
        ),
        migrations.AlterField(
            model_name='imp_value',
            name='property',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='prop.Property'),
        ),
        migrations.DeleteModel(
            name='Src',
        ),
        migrations.DeleteModel(
            name='Src_Imp',
        ),
    ]
