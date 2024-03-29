# Generated by Django 4.0.5 on 2022-07-04 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0005_alter_user_bot_language'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='interested_in',
            field=models.IntegerField(choices=[(0, 'Boys'), (1, 'Girls'), (2, 'All')], default=1),
        ),
        migrations.AddField(
            model_name='user',
            name='location_lat',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='location_lon',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='location_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='name',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, 'Male'), (1, 'Female')], default=0),
        ),
    ]
