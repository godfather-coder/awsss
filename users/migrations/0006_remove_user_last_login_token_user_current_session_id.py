# Generated by Django 4.2.7 on 2024-08-26 20:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_user_last_login_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='last_login_token',
        ),
        migrations.AddField(
            model_name='user',
            name='current_session_id',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]
