# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_author_github_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='github_etag',
            field=models.CharField(max_length=64, blank=True),
            preserve_default=True,
        ),
    ]
