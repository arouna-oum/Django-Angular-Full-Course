from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Books(models.Model):
    name = models.TextField(blank=True, null=True, max_length=30)
    resume = models.FileField()
    user = models.ManyToManyField(User, related_name="user_books")
    created_at = models.DateTimeField(auto_now=datetime.now)
