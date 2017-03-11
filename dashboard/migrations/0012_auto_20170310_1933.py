# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-11 02:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_node'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='service_url',
            field=models.URLField(unique=True),
        ),
        migrations.AlterField(
            model_name='node',
            name='website_url',
            field=models.URLField(unique=True),
        ),
    ]
