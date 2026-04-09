from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('recommendations.Book', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('recommendations.Book', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('recommendations.Book', on_delete=models.CASCADE)
    score = models.IntegerField()  # 1-5
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'book')


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('recommendations.Book', on_delete=models.CASCADE)
    content = models.TextField(max_length=500)
    rating = models.IntegerField(null=True, blank=True)
    likes_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)


class CommentLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'comment')


class BrowsingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey('recommendations.Book', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now=True)