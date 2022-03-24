# Generated by Django 4.0.2 on 2022-03-24 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_rename_imgcontent_post_img_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='context',
            field=models.URLField(default=''),
        ),
        migrations.AddField(
            model_name='like',
            name='object',
            field=models.JSONField(default=dict, max_length=500),
        ),
        migrations.AddField(
            model_name='like',
            name='summary',
            field=models.TextField(default=''),
        ),
    ]
