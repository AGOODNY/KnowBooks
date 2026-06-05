from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import *

router = DefaultRouter()

router.register(
    r'books',
    BookViewSet,
    basename='books'
)

router.register(
    r'tags',
    TagViewSet,
    basename='tags'
)

urlpatterns = [

    path(
        'home/',
        HomeView.as_view()
    ),

    path(
        'search/',
        SearchView.as_view()
    ),

    path(
        'book/<int:book_id>/',
        BookDetailView.as_view()
    ),

    path(
        '',
        include(router.urls)
    ),
]