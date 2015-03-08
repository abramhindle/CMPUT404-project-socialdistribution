# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0004_friendrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='requestee',
            field=models.ForeignKey(related_name='friend_requests_s', to='author.Author'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='requester',
            field=models.ForeignKey(related_name='friend_requests_r', to='author.Author'),
            preserve_default=True,
        ),
    ]
