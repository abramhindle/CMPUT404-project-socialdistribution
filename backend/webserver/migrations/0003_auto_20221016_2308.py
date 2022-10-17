# Generated by Django 3.1.6 on 2022-10-16 23:08

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0002_alter_author_id_alter_follow_followee_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(verbose_name='created_at')),
                ('content_type', models.CharField(choices=[('text/plain', 'Plain text'), ('text/markdown', 'Markdown text')], default='text/plain', max_length=200)),
            ],
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='followrequest',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='date created')),
                ('edited_at', models.DateTimeField(verbose_name='date edited')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('source', models.CharField(max_length=200)),
                ('origin', models.CharField(max_length=200)),
                ('unlisted', models.BooleanField(default=False)),
                ('visibility', models.CharField(choices=[('PUBLIC', 'Public'), ('FRIENDS', 'Friends')], default='PUBLIC', max_length=200)),
                ('content_type', models.CharField(choices=[('text/plain', 'Plain text'), ('text/markdown', 'Markdown text')], default='text/plain', max_length=200)),
                ('content', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webserver.author')),
            ],
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webserver.author')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webserver.comment')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webserver.post')),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webserver.author'),
        ),
        migrations.AddField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webserver.post'),
        ),
    ]
