# Generated by Django 2.1.5 on 2019-02-26 23:51

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('posts', '0003_auto_20190222_0019'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='displayName',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
