# Generated by Django 5.1 on 2024-10-12 18:59

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Books', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='books',
            name='user',
            field=models.ManyToManyField(related_name='user_books', to=settings.AUTH_USER_MODEL),
        ),
    ]
