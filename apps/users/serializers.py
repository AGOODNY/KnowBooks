from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.interactions.models import Comment

User = get_user_model()


# 注册
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# 用户信息
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'nickname', 'avatar',
                  'books_read_count', 'likes_count', 'favorites_count',
                  'is_staff', 'is_superuser'
                  ]


# 我的评论
class MyCommentSerializer(serializers.ModelSerializer):
    book_title = serializers.CharField(source='book.title', read_only=True)
    book_cover = serializers.CharField(source='book.cover', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'book_id', 'book_title', 'book_cover', 'content',
                  'rating', 'created_at', 'likes_count', 'username']

# 修改信息
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'avatar']


# 修改密码
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        user = self.context['request'].user
        if not user.check_password(data['old_password']):
            raise serializers.ValidationError("Old password incorrect")
        return data

