# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
        ('post', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(unique=True, max_length=128)),
                ('comment', models.TextField()),
                ('pubDate', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to='author.Author')),
                ('post', models.ForeignKey(to='post.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
