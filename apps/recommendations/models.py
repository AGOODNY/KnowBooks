from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    cover = models.URLField(blank=True)

    tags = models.ManyToManyField(Tag, related_name='books', blank=True)

    # 统计字段（由 interactions 更新或查询）
    likes_count = models.IntegerField(default=0)
    favorites_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title