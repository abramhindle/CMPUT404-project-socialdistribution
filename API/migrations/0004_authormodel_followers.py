# Generated by Django 4.1.6 on 2023-02-25 21:03

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0003_authormodel_github_authormodel_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='authormodel',
            name='followers',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.JSONField(blank=True, max_length=100), blank=True, default=list, size=None),
        ),
    ]
