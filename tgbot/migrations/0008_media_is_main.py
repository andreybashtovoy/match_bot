# Generated by Django 4.0.5 on 2022-07-11 17:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0007_media'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='is_main',
            field=models.BooleanField(default=False),
        ),
    ]