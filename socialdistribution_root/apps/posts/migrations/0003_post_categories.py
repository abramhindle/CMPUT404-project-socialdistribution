# Generated by Django 3.2.9 on 2021-11-21 22:34

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20211121_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='categories',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), default=list, size=None),
        ),
    ]
