# Generated by Django 4.1.7 on 2023-03-01 01:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_rename_comments_comment_rename_likes_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content_type',
            new_name='contentType',
        ),
    ]
