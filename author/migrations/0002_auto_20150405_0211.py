# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='friendrequest',
            name='status',
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='followStatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='frStatus',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='friendrequest',
            name='requestStatus',
            field=models.BooleanField(default=False),
        ),
    ]
