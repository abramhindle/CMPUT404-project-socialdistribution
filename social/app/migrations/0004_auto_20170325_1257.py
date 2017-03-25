# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-03-25 18:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_post_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='visible_to',
            field=models.ManyToManyField(blank=True, related_name='visible_posts', to='app.Author'),
        ),
    ]
