# Generated by Django 3.2 on 2023-03-23 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('service', '0007_author_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inbox',
            name='comments',
            field=models.ManyToManyField(blank=True, to='service.Comment'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='follow_requests',
            field=models.ManyToManyField(blank=True, to='service.Follow'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='likes',
            field=models.ManyToManyField(blank=True, to='service.Like'),
        ),
        migrations.AlterField(
            model_name='inbox',
            name='posts',
            field=models.ManyToManyField(blank=True, to='service.Post'),
        ),
    ]
