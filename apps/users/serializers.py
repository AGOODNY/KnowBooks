from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import EmailVerificationCode

User = get_user_model()


# 注册
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    code = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'username', 'password', 'code']

    def validate(self, data):
        email = data['email']
        code = data['code']

        record = EmailVerificationCode.objects.filter(
            email=email, code=code, is_used=False
        ).order_by('-created_at').first()

        if not record:
            raise serializers.ValidationError("Invalid verification code")

        record.is_used = True
        record.save()

        return data

    def create(self, validated_data):
        validated_data.pop('code')
        user = User.objects.create_user(**validated_data)
        return user


# 用户信息
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'nickname', 'avatar',
                  'books_read_count', 'likes_count', 'favorites_count']


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