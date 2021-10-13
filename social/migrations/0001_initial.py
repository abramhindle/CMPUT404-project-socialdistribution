# Generated by Django 3.2.8 on 2021-10-13 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('host', models.URLField()),
                ('url', models.URLField()),
                ('display_name', models.CharField(max_length=200)),
                ('github_url', models.URLField()),
                ('followers', models.ManyToManyField(blank=True, related_name='follower', to='social.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('url', models.URLField(max_length=500)),
                ('title', models.CharField(max_length=200)),
                ('source', models.URLField()),
                ('origin', models.URLField()),
                ('description', models.CharField(max_length=240)),
                ('contentType', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], max_length=30)),
                ('content', models.TextField(max_length=2000)),
                ('published', models.DateTimeField(verbose_name='date published')),
                ('visibility', models.CharField(choices=[('PUBLIC', 'PUBLIC'), ('FOLLOWERS', 'FOLLOWERS'), ('PRIVATE', 'PRIVATE')], max_length=30)),
                ('unlisted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.author')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('contentType', models.CharField(choices=[('text/markdown', 'text/markdown'), ('text/plain', 'text/plain'), ('application/base64', 'application/base64'), ('image/png;base64', 'image/png;base64'), ('image/jpeg;base64', 'image/jpeg;base64')], default='text/plain', max_length=30)),
                ('comment', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='social.post')),
            ],
        ),
        migrations.CreateModel(
            name='PostLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.post')),
            ],
            options={
                'unique_together': {('author', 'post')},
            },
        ),
        migrations.CreateModel(
            name='CommentLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('summary', models.CharField(max_length=200)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.author')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='social.comment')),
            ],
            options={
                'unique_together': {('author', 'comment')},
            },
        ),
    ]
