# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-27 01:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WAMAStucco', '0009_auto_20170326_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='position',
            field=models.CharField(choices=[('NA', 'None'), ('CU', 'Cutting'), ('MO', 'Moulding'), ('IN', 'Installing')], default='NA', max_length=2),
        ),
    ]
