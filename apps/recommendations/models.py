from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL


class Tag(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True
    )

    def __str__(self):
        return self.name


class Book(models.Model):

    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(max_length=255)

    author = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    cover = models.URLField(blank=True)

    tags = models.ManyToManyField(
        Tag,
        related_name='books',
        blank=True
    )

    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='uploaded_books',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    likes_count = models.IntegerField(default=0)

    favorites_count = models.IntegerField(default=0)

    average_rating = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )

    def __str__(self):
        return self.title