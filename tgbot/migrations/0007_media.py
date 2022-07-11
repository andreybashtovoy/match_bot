# Generated by Django 4.0.5 on 2022-07-11 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tgbot', '0006_user_active_user_age_user_interested_in_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('file_id', models.CharField(max_length=256, primary_key=True, serialize=False)),
                ('media_type', models.IntegerField(choices=[(0, 'Photo'), (1, 'Video')])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='media', to='tgbot.user')),
            ],
            options={
                'ordering': ('-created_at',),
                'abstract': False,
            },
        ),
    ]