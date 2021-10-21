# Generated by Django 3.2.7 on 2021-10-19 04:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('authors', '0017_alter_author_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=200, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='inboxobject',
            name='object_id',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
