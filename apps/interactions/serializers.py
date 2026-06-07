# apps/interactions/serializers.py
from rest_framework import serializers
from .models import *


class CommentSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    avatar = serializers.CharField(source='user.avatar', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'book', 'content', 'rating', 'created_at', 'likes_count', 'username', 'avatar']
        read_only_fields = ['id', 'user', 'book', 'created_at', 'likes_count', 'username', 'avatar']
        extra_kwargs = {
            'rating': {'required': False, 'allow_null': True}
        }

    def create(self, validated_data):
        return Comment.objects.create(**validated_data)