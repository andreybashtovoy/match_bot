# Generated by Django 4.0.5 on 2022-08-03 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0009_user_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='link',
            field=models.CharField(default='', max_length=512),
        ),
    ]