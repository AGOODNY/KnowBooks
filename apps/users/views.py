from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import EmailVerificationCode
from .serializers import *

from apps.interactions.models import (
    Favorite, Like, Comment, BrowsingHistory
)

User = get_user_model()


# 发送验证码
class SendCodeView(APIView):
    def post(self, request):
        email = request.data.get('email')

        code = '123456'  # 开发阶段先写死（后面换随机+邮箱发送）

        EmailVerificationCode.objects.create(email=email, code=code)

        return Response({"msg": "code sent", "code": code})

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
        data = Favorite.objects.filter(user=request.user)
        return Response([f.book.id for f in data])

#我的点赞
class MyLikesView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = Like.objects.filter(user=request.user)
        return Response([l.book.id for l in data])

#我的评论
class MyCommentsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = Comment.objects.filter(user=request.user)
        return Response([
            {
                "book_id": c.book.id,
                "content": c.content
            } for c in data
        ])

# 浏览历史
class MyHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = BrowsingHistory.objects.filter(user=request.user)
        return Response([h.book.id for h in data])

#统计信息
class UserStatsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response({
            "favorites": user.favorites_count,
            "likes": user.likes_count,
            "books_read": user.books_read_count,
        })
