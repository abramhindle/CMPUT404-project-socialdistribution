# Generated by Django 4.1.5 on 2023-03-22 21:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('author', '0015_remove_node_last_login_remove_node_password_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='node',
            name='url',
            field=models.URLField(default='https://sociallydistributed.herokuapp.com/', editable=False, max_length=500),
        ),
        migrations.AddField(
            model_name='node',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='node',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=255, primary_key=True, serialize=False),
        ),
    ]
