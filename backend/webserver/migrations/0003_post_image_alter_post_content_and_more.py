# Generated by Django 4.1.2 on 2022-12-03 03:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webserver', '0002_alter_node_team'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='content_type',
            field=models.CharField(choices=[('text/plain', 'Plain text'), ('text/markdown', 'Markdown text'), ('image/png;base64', 'PNG image'), ('image/jpeg;base64', 'JPEG image')], default='text/plain', max_length=200),
        ),
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, default=''),
        ),
        migrations.AlterField(
            model_name='post',
            name='title',
            field=models.CharField(default='', max_length=300),
        ),
    ]
