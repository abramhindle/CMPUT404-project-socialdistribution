# Generated by Django 4.0.2 on 2022-03-22 02:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('follow', '0003_alter_follow_created_alter_request_created'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='follow',
            name='true_friend',
        ),
    ]
