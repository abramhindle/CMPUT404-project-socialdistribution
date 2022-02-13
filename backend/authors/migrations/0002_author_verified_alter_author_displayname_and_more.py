# Generated by Django 4.0.2 on 2022-02-13 09:07

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='author',
            name='verified',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='author',
            name='displayName',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='author',
            name='local_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
