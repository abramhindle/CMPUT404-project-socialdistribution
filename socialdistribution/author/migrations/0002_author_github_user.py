# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='github_user',
            field=models.CharField(max_length=128, blank=True),
            preserve_default=True,
        ),
    ]
