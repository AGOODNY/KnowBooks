from django.db.models import Avg
from apps.recommendations.models import Book
from .models import Like, Favorite, Rating


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