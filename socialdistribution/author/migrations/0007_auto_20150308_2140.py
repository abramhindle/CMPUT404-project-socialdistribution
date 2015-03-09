# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0006_friendrequest_requeststatus'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendrequest',
            name='requestee',
            field=models.ForeignKey(related_name='friend_requests_s', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='requester',
            field=models.ForeignKey(related_name='friend_requests_r', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
    ]
