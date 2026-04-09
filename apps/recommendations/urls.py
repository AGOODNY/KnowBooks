from django.urls import path
from .views import *

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('search/', SearchView.as_view()),
    path('book/<int:book_id>/', BookDetailView.as_view()),
]