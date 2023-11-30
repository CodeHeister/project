from django.contrib.auth import get_user_model

from rest_framework import serializers

User = get_user_model()

class UserSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField(max_length=100)
    username = serializers.CharField(max_length=100)
    friends = serializers.JSONField()

class FriendSerializer(serializers.Serializer):
    id = serializers.UUIDField()
