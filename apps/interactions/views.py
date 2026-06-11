from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import *
from .serializers import CommentSerializer
from django.db.models import Avg
from .services import (
    update_book_like_count,
    update_user_like_count,
    update_book_favorite_count,
    update_book_rating,
    update_user_favorite_count,
    update_user_comment_count
)
from ..recommendations.models import Book


#点赞与取消点赞
class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id):
        is_liked = Like.objects.filter(user=request.user, book_id=book_id).exists()
        book = Book.objects.get(id=book_id)
        return Response({
            "is_liked": is_liked,
            "likes_count": book.likes_count
        })

    def post(self, request, book_id):
        obj, created = Like.objects.get_or_create(
            user=request.user,
            book_id=book_id
        )

        if not created:
            obj.delete()

        update_book_like_count(book_id)
        update_user_like_count(request.user.id)

        return Response({
            "msg": "unliked" if not created else "liked"
        })


class ToggleFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, book_id):
        is_favorited = Favorite.objects.filter(user=request.user, book_id=book_id).exists()
        return Response({
            "is_favorited": is_favorited
        })

    def post(self, request, book_id):
        obj, created = Favorite.objects.get_or_create(
            user=request.user,
            book_id=book_id
        )

        if not created:
            obj.delete()

        update_book_favorite_count(book_id)
        update_user_favorite_count(request.user.id)

        return Response({
            "msg": "unfavorited" if not created else "favorited"
        })

#评分
class RateBookView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):

        score = int(request.data.get('score', 0))

        if score < 1 or score > 5:
            return Response(
                {"error": "score must be 1-5"},
                status=400
            )

        Rating.objects.update_or_create(
            user=request.user,
            book_id=book_id,
            defaults={'score': score}
        )

        update_book_rating(book_id)

        avg = Rating.objects.filter(
            book_id=book_id
        ).aggregate(
            avg=Avg('score')
        )

        return Response({
            "avg_score": avg['avg']
        })

#评论
class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        print(f"Received comment request - book_id: {book_id}")
        print(f"Request data: {request.data}")

        serializer = CommentSerializer(data={
            'content': request.data.get('content', '')
        })

        if not serializer.is_valid():
            print(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=400)
        comment = serializer.save(
            user=request.user,
            book_id=book_id
        )

        update_user_comment_count(request.user.id)

        return Response(CommentSerializer(comment).data, status=201)



# 获取评论列表
class CommentListView(APIView):
    def get(self, request, book_id):
        comments = Comment.objects.filter(book_id=book_id).order_by('-created_at')

        result = []
        for comment in comments:
            rating = None
            try:
                rating_obj = Rating.objects.get(user=comment.user, book_id=book_id)
                rating = rating_obj.score
            except Rating.DoesNotExist:
                rating = comment.rating

            avatar_url = ''
            if comment.user.avatar:
                if hasattr(comment.user.avatar, 'url'):
                    avatar_url = comment.user.avatar.url
                elif isinstance(comment.user.avatar, str):
                    avatar_url = comment.user.avatar
                else:
                    avatar_url = ''

            result.append({
                "id": comment.id,
                "username": comment.user.username,
                "avatar": avatar_url,
                "content": comment.content,
                "rating": rating,
                "created_at": comment.created_at,
                "likes_count": comment.likes_count
            })

        return Response(result)


#给评论点赞
class ToggleCommentLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        obj, created = CommentLike.objects.get_or_create(
            user=request.user,
            comment_id=comment_id
        )

        comment = Comment.objects.get(id=comment_id)

        if not created:
            obj.delete()
            comment.likes_count -= 1
            comment.save()
            return Response({"msg": "unliked"})

        comment.likes_count += 1
        comment.save()

        return Response({"msg": "liked"})

#浏览历史
class AddHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        BrowsingHistory.objects.update_or_create(
            user=request.user,
            book_id=book_id
        )

        return Response({"msg": "added"})

#获取历史
class HistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        data = BrowsingHistory.objects.filter(user=request.user).order_by('-created_at')
        return Response([h.book.id for h in data])

#清空历史
class ClearHistoryView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        BrowsingHistory.objects.filter(user=request.user).delete()
        return Response({"msg": "cleared"})