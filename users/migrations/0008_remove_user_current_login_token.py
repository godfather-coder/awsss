# Generated by Django 4.2.7 on 2024-08-26 21:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0007_remove_user_current_session_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='current_login_token',
        ),
    ]
