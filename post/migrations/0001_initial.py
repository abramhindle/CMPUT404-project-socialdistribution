# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0001_initial'),
        ('images', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guid', models.CharField(unique=True, max_length=64)),
                ('title', models.CharField(max_length=128)),
                ('description', models.CharField(max_length=512)),
                ('content', models.TextField()),
                ('visibility', models.CharField(default=b'public', max_length=20)),
                ('content_type', models.CharField(default=b'text/plain', max_length=100)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('last_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(to='author.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PostImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ForeignKey(to='images.Image')),
                ('post', models.ForeignKey(to='post.Post')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='VisibleToAuthor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('post', models.ForeignKey(to='post.Post')),
                ('visibleAuthor', models.ForeignKey(to='author.Author')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
