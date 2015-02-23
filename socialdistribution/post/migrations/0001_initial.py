# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post_id', models.IntegerField(unique=True)),
                ('text', models.TextField()),
                ('visibility', models.CharField(default=b'public', max_length=20, choices=[(b'self', b'Self'), (b'author', b'Another_Author'), (b'friend', b'Friends'), (b'friendsOfFriends', b'Friends_Of_Friends'), (b'friendsOwnHost', b'Friends_Own_Host'), (b'public', b'Public')])),
                ('mime_type', models.CharField(default=b'text/plain', max_length=100)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
