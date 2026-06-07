from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *

from apps.interactions.models import (
    Favorite, Like, Comment, BrowsingHistory, Rating
)
from ..recommendations.serializers import BookSerializer

User = get_user_model()


# 注册
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"msg": "register success"})

#登陆
class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=400)

        if user.is_banned:
            return Response({"error": "User banned"}, status=403)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        })

#管理员登陆
class AdminLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = User.objects.filter(email=email).first()

        if not user or not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=400)

        if not user.is_staff:
            return Response({"error": "Not admin"}, status=403)

        refresh = RefreshToken.for_user(user)

        return Response({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "is_admin": True
        })


# 当前用户信息
class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)

#修改当前用户信息
class UpdateProfileView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def put(self, request):
        serializer = UpdateUserSerializer(
            request.user, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

#修改密码
class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data, context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()

        return Response({"msg": "password updated"})



# 个人中心
# 我的收藏
class MyFavoritesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        favorites = Favorite.objects.filter(user=request.user).select_related('book')
        books = [fav.book for fav in favorites]
        serializer = BookSerializer(books, many=True, context={'request': request})
        return Response(serializer.data)
#我的点赞
class MyLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = Like.objects.filter(user=request.user)
        return Response([l.book.id for l in data])

# 我的评论
class MyCommentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        comments = Comment.objects.filter(user=request.user).select_related('book', 'user')

        result = []
        for comment in comments:
            cover_url = None
            if comment.book and comment.book.cover:
                if isinstance(comment.book.cover, str):
                    cover_url = comment.book.cover
                elif hasattr(comment.book.cover, 'url'):
                    cover_url = comment.book.cover.url

            # 获取评分
            rating = comment.rating
            if rating is None:
                try:
                    rating_obj = Rating.objects.get(user=request.user, book=comment.book)
                    rating = rating_obj.score
                except Rating.DoesNotExist:
                    rating = 0

            result.append({
                "id": comment.id,
                "book_id": comment.book.id,
                "book_title": comment.book.title,
                "book_cover": cover_url,
                "content": comment.content,
                "rating": rating,
                "created_at": comment.created_at,
                "likes_count": comment.likes_count,
                "username": comment.user.username,
            })

        return Response(result)

# 浏览历史
class MyHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = BrowsingHistory.objects.filter(user=request.user)
        return Response([h.book.id for h in data])

class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        # 获取用户的评论数量
        comments_count = Comment.objects.filter(user=user).count()
        # 获取浏览历史数量
        books_read_count = BrowsingHistory.objects.filter(user=user).values('book').distinct().count()

        return Response({
            "favorites": user.favorites_count,
            "likes": user.likes_count,
            "books_read": books_read_count,
            "comments": comments_count,
        })