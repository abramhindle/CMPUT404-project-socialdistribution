# Generated by Django 3.1.6 on 2021-10-12 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('author', '0002_auto_20211011_1852'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='host',
            field=models.URLField(),
        ),
    ]
