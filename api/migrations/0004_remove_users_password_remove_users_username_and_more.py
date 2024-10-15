# Generated by Django 5.1 on 2024-08-22 09:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_users_confirm_password_alter_users_password_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='password',
        ),
        migrations.RemoveField(
            model_name='users',
            name='username',
        ),
        migrations.AddField(
            model_name='users',
            name='phone_number',
            field=models.IntegerField(blank=True, default=0, max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='users',
            name='profil_picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='users',
            name='user',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='users',
            name='confirm_password',
            field=models.CharField(blank=True, max_length=8, null=True),
        ),
    ]