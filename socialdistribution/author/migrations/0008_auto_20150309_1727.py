# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0007_auto_20150308_2140'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friendrequest',
            old_name='requestStatus',
            new_name='status',
        ),
    ]
