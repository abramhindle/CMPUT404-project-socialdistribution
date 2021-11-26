# Generated by Django 3.2.9 on 2021-11-25 19:54

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_author_isapproved'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='author',
            name='followers',
        ),
        migrations.AlterField(
            model_name='author',
            name='id',
            field=models.CharField(default=uuid.uuid4, editable=False, max_length=200, primary_key=True, serialize=False, unique=True),
        ),
        migrations.CreateModel(
            name='Followers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.ForeignKey(db_column='follower', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='follows', to='core.author')),
                ('target', models.ForeignKey(db_column='target', db_constraint=False, on_delete=django.db.models.deletion.CASCADE, related_name='is_followed', to='core.author')),
            ],
        ),
    ]
