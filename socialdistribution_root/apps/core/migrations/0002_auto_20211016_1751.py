# Generated by Django 3.2.7 on 2021-10-16 17:51

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AddField(
            model_name='user',
            name='displayName',
            field=models.CharField(blank=True, max_length=80, verbose_name='displayName'),
        ),
        migrations.AddField(
            model_name='user',
            name='profileImage',
            field=models.URLField(blank=True, verbose_name='profileImage'),
        ),
        migrations.AddField(
            model_name='user',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='github',
            field=models.URLField(blank=True, max_length=80, verbose_name='github'),
        ),
    ]
