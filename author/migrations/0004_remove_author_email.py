# Generated by Django 3.2.8 on 2021-10-19 01:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0003_auto_20211018_1743'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='email',
        ),
    ]
