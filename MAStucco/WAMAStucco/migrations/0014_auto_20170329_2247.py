# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-30 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WAMAStucco', '0013_auto_20170326_2152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='partorder',
            name='quantity',
            field=models.PositiveIntegerField(blank=True),
        ),
    ]
