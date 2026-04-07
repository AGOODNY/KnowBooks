from django.urls import path
from .views import *

urlpatterns = [
    path('send-code/', SendCodeView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('admin/login/', AdminLoginView.as_view()),

    path('me/', MeView.as_view()),
    path('update/', UpdateProfileView.as_view()),
    path('change-password/', ChangePasswordView.as_view()),

    path('favorites/', MyFavoritesView.as_view()),
    path('likes/', MyLikesView.as_view()),
    path('comments/', MyCommentsView.as_view()),
    path('history/', MyHistoryView.as_view()),

    path('stats/', UserStatsView.as_view()),
]