# Generated by Django 3.2.8 on 2021-10-22 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0012_auto_20211016_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='profile_image',
            field=models.URLField(blank=True),
        ),
    ]
