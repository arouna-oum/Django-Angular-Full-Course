from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Note, Users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username","password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ["id","username","password","confirm_password"]

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = "__all__"
        extra_kwargs = {"author": {"read_only": True}}