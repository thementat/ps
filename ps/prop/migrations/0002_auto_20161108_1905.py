# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-08 19:05
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('prop', '0001_initial'),
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
        migrations.DeleteModel(
            name='Src',
        ),
        migrations.DeleteModel(
            name='Src_Imp',
        ),
    ]
