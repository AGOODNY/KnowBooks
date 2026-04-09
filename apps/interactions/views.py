from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import *
from .serializers import CommentSerializer
from django.db.models import Avg

#点赞与取消点赞
class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        obj, created = Like.objects.get_or_create(
            user=request.user,
            book_id=book_id
        )

        if not created:
            obj.delete()
            return Response({"msg": "unliked"})

        return Response({"msg": "liked"})

#收藏和取消收藏
class ToggleFavoriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        obj, created = Favorite.objects.get_or_create(
            user=request.user,
            book_id=book_id
        )

        if not created:
            obj.delete()
            return Response({"msg": "unfavorited"})

        return Response({"msg": "favorited"})

#评分
class RateBookView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        score = int(request.data.get('score'))

        Rating.objects.update_or_create(
            user=request.user,
            book_id=book_id,
            defaults={'score': score}
        )

        avg = Rating.objects.filter(book_id=book_id).aggregate(avg=Avg('score'))

        return Response({"avg_score": avg['avg']})

#评论
class CommentView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, book_id):
        serializer = CommentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        serializer.save(user=request.user, book_id=book_id)

        return Response(serializer.data)

#获取评论列表
class CommentListView(APIView):
    def get(self, request, book_id):
        comments = Comment.objects.filter(book_id=book_id).order_by('-created_at')
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)


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