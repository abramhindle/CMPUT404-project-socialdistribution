# Generated by Django 2.1.5 on 2020-03-10 04:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_auto_20200308_0539'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='authorfriend',
            unique_together={('author', 'friend')},
        ),
    ]
