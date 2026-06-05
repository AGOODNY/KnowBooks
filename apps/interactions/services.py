from django.db.models import Avg
from apps.recommendations.models import Book
from django.contrib.auth import get_user_model

from .models import Like, Favorite, Rating, Comment

User = get_user_model()

def update_book_like_count(book_id):

    count = Like.objects.filter(
        book_id=book_id
    ).count()

    Book.objects.filter(
        id=book_id
    ).update(
        likes_count=count
    )


def update_book_favorite_count(book_id):

    count = Favorite.objects.filter(
        book_id=book_id
    ).count()

    Book.objects.filter(
        id=book_id
    ).update(
        favorites_count=count
    )


def update_book_rating(book_id):

    avg = Rating.objects.filter(
        book_id=book_id
    ).aggregate(
        avg=Avg("score")
    )["avg"]

    Book.objects.filter(
        id=book_id
    ).update(
        average_rating=avg or 0
    )

def update_user_like_count(user_id):

    count = Like.objects.filter(
        user_id=user_id
    ).count()

    User.objects.filter(
        id=user_id
    ).update(
        likes_count=count
    )

def update_user_favorite_count(user_id):

    count = Favorite.objects.filter(
        user_id=user_id
    ).count()

    User.objects.filter(
        id=user_id
    ).update(
        favorites_count=count
    )

def update_user_comment_count(user_id):

    count = Comment.objects.filter(
        user_id=user_id
    ).count()

    User.objects.filter(
        id=user_id
    ).update(
        comments_count=count
    )