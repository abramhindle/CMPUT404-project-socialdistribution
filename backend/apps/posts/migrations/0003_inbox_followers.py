# Generated by Django 4.1.6 on 2023-03-01 20:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_alter_author_profileimage'),
        ('posts', '0002_alter_post_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Inbox',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authors.author')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.post')),
            ],
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('dateTime', models.DateTimeField(auto_now_add=True)),
                ('followers', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to='authors.author')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner', to='authors.author')),
            ],
        ),
    ]
