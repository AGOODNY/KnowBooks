from django.urls import path
from .views import *

urlpatterns = [
    path('like/<int:book_id>/', ToggleLikeView.as_view()),
    path('favorite/<int:book_id>/', ToggleFavoriteView.as_view()),
    path('rate/<int:book_id>/', RateBookView.as_view()),

    path('comment/<int:book_id>/', CommentView.as_view()),
    path('comments/<int:book_id>/', CommentListView.as_view()),

    path('comment-like/<int:comment_id>/', ToggleCommentLikeView.as_view()),

    path('history/add/<int:book_id>/', AddHistoryView.as_view()),
    path('history/', HistoryView.as_view()),
    path('history/clear/', ClearHistoryView.as_view()),
]