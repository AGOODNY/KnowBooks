from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

from .models import Book
from .serializers import BookSerializer

from apps.interactions.models import Like, Favorite
from django.db.models import Q

#首页接口
class HomeView(APIView):
    def get(self, request):
        strategy = request.GET.get('type', 'hot')
        user = request.user if request.user.is_authenticated else None

        # 热门
        if strategy == 'hot':
            books = Book.objects.order_by('-likes_count', '-favorites_count')[:10]

        # 最新
        elif strategy == 'latest':
            books = Book.objects.order_by('-created_at')[:10]

        # 个性化推荐
        elif strategy == 'recommend' and user:
            books = self.recommend_books(user)

        else:
            books = Book.objects.order_by('-likes_count')[:10]

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


#协同过滤
    def recommend_books(self, user):
        # 用户喜欢的书
        liked_books = Like.objects.filter(user=user).values_list('book_id', flat=True)
        fav_books = Favorite.objects.filter(user=user).values_list('book_id', flat=True)

        user_books = set(list(liked_books) + list(fav_books))

        if not user_books:
            return Book.objects.order_by('-likes_count')[:10]

        # 找“相似用户”
        similar_users = Like.objects.filter(
            book_id__in=user_books
        ).exclude(user=user).values_list('user_id', flat=True)

        # 找这些用户喜欢的书
        recommended_books = Like.objects.filter(
            user_id__in=similar_users
        ).exclude(book_id__in=user_books).values_list('book_id', flat=True)

        return Book.objects.filter(id__in=recommended_books)[:10]

#搜索
class SearchView(APIView):
    def get(self, request):
        keyword = request.GET.get('q', '')

        books = Book.objects.filter(
            Q(title__icontains=keyword) |
            Q(author__icontains=keyword) |
            Q(tags__name__icontains=keyword)
        ).distinct()

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

#书籍详情
class BookDetailView(APIView):
    def get(self, request, book_id):
        book = Book.objects.get(id=book_id)

        data = BookSerializer(book).data

        # 如果登录 → 返回用户状态
        if request.user.is_authenticated:
            from apps.interactions.models import Like, Favorite

            data['liked'] = Like.objects.filter(
                user=request.user, book=book
            ).exists()

            data['favorited'] = Favorite.objects.filter(
                user=request.user, book=book
            ).exists()

        return Response(data)