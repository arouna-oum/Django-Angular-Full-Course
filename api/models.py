from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Users(models.Model):
    # user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=30, null=True, blank=False)
    password = models.CharField(max_length=8, null=True, blank=False)
    confirm_password = models.CharField(max_length=8, null=True, blank=False)
    profil_picture = models.ImageField(null=True, blank=True)
    phone_number = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"the user is {self.username}"

class Note(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    def __str__(self):
        return self.title