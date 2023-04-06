# Generated by Django 4.1.6 on 2023-03-24 03:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('author', '0012_remove_followrequest_summary_followrequest_summary'),
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=30)),
                ('name', models.CharField(default='Node', max_length=255)),
                ('is_active', models.BooleanField(default=False)),
                ('url', models.URLField(default='https://sociallydistributed.herokuapp.com/', editable=False, max_length=500)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'Node',
            },
        ),
    ]
