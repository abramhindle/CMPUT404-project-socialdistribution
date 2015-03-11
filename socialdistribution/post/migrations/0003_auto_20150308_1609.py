# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_auto_20150308_0053'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='mime_type',
            field=models.CharField(default='text/plain', max_length=100),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='post',
            name='visibility',
            field=models.CharField(default='public', max_length=20),
            preserve_default=True,
        ),
    ]
