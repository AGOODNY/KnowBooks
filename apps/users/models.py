from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)

    nickname = models.CharField(max_length=50, blank=True)
    avatar = models.URLField(blank=True)

    # 统计字段（冗余字段，提高查询性能）
    books_read_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    favorites_count = models.PositiveIntegerField(default=0)
    comments_count = models.PositiveIntegerField(default=0)
    # 权限 / 状态
    is_email_verified = models.BooleanField(default=False)
    is_banned = models.BooleanField(default=False)

    # 登录方式
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email


# 邮箱验证码（注册用）
class EmailVerificationCode(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)

    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.email} - {self.code}"