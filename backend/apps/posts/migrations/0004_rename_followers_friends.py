# Generated by Django 4.1.6 on 2023-03-01 21:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0002_alter_author_profileimage'),
        ('posts', '0003_inbox_followers'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Followers',
            new_name='Friends',
        ),
    ]
