# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0005_auto_20150308_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='friendrequest',
            name='requestStatus',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
