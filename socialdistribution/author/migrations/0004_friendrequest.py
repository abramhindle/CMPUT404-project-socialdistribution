# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_author_github_etag'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('requestee', models.ForeignKey(related_name='friend_requests_r', to='author.Author')),
                ('requester', models.ForeignKey(related_name='friend_requests_s', to='author.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
