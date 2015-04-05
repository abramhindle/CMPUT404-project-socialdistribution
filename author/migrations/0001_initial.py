# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('uuid', models.CharField(default=uuid.uuid4, unique=True, max_length=256)),
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('github_user', models.CharField(max_length=128, blank=True)),
                ('host', models.CharField(default=b'social-distribution.herokuapp.com', max_length=128)),
                ('url', models.CharField(max_length=256, blank=True)),
                ('github_etag', models.CharField(max_length=64, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('frStatus', models.BooleanField(default=False)),
                ('requestStatus', models.BooleanField(default=False)),
                ('followStatus', models.BooleanField(default=False)),
                ('requestee', models.ForeignKey(related_name='friend_requests_s', to='author.Author')),
                ('requester', models.ForeignKey(related_name='friend_requests_r', to='author.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
