# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2019-02-16 04:10
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorProfile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('host', models.URLField()),
                ('displayName', models.CharField(max_length=100)),
                ('github', models.URLField()),
                ('bio', models.CharField(max_length=1024)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('name', models.CharField(max_length=100, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('comment', models.TextField(max_length=2097152)),
                ('contentType', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=20)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('FOLLOWING', 'FOLLOWING'), ('FRIENDS', 'FRIENDS'), ('DECLINED', 'DECLINED')], default='FOLLOWING', max_length=10)),
                ('authorA', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_A', to=settings.AUTH_USER_MODEL)),
                ('authorB', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_B', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('title', models.CharField(max_length=1024)),
                ('source', models.CharField(max_length=1024)),
                ('origin', models.CharField(max_length=1024)),
                ('description', models.CharField(max_length=1024)),
                ('contentType', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=20)),
                ('content', models.TextField(max_length=2097152)),
                ('published', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FOAF', 'FOAF'), ('FRIENDS', 'FRIENDS'), ('PRIVATE', 'PRIVATE'), ('SERVERONLY', 'SERVERONLY')], default='PRIVATE', max_length=10)),
                ('unlisted', models.BooleanField(default=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to=settings.AUTH_USER_MODEL)),
                ('categories', models.ManyToManyField(to='api.Category')),
                ('visibleTo', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='api.Post'),
        ),
    ]
