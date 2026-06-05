from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone

from .models import Book, Tag
from .serializers import (
    BookSerializer,
    TagSerializer
)

from .permissions import IsAdminUser
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

#新增
class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()

    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(
            uploaded_by=self.request.user
        )

    def get_queryset(self):
        queryset = Book.objects.all()

        keyword = self.request.GET.get(
            "keyword"
        )

        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword)
                |
                Q(author__icontains=keyword)
                |
                Q(tags__name__icontains=keyword)
            ).distinct()

        return queryset

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser]
    )
    def approve(self, request, pk=None):
        book = self.get_object()

        book.status = "approved"

        book.approved_at = timezone.now()

        book.save()

        return Response({
            "message": "Book approved"
        })

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser]
    )
    def reject(self, request, pk=None):
        book = self.get_object()

        book.status = "rejected"

        book.save()

        return Response({
            "message": "Book rejected"
        })

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAdminUser]
    )
    def pending(self, request):
        books = Book.objects.filter(
            status="pending"
        )

        serializer = BookSerializer(
            books,
            many=True
        )

        return Response(
            serializer.data
        )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsAuthenticated]
    )
    def my_uploads(self, request):
        books = Book.objects.filter(
            uploaded_by=request.user
        )

        serializer = BookSerializer(
            books,
            many=True
        )

        return Response(
            serializer.data
        )

    #新增
class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()

    serializer_class = TagSerializer