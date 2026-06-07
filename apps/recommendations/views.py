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
from django.db.models import Count
from django.core.paginator import Paginator

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

        liked_books = Like.objects.filter(
            user=user
        ).values_list(
            'book_id',
            flat=True
        )

        fav_books = Favorite.objects.filter(
            user=user
        ).values_list(
            'book_id',
            flat=True
        )

        user_books = set(
            list(liked_books)
            +
            list(fav_books)
        )

        if not user_books:
            return Book.objects.filter(
                status="approved"
            ).order_by(
                '-likes_count'
            )[:10]

        similar_users = Like.objects.filter(
            book_id__in=user_books
        ).exclude(
            user=user
        ).values_list(
            'user_id',
            flat=True
        )

        collaborative_ids = Like.objects.filter(
            user_id__in=similar_users
        ).exclude(
            book_id__in=user_books
        ).values_list(
            'book_id',
            flat=True
        )

        preferred_tags = Tag.objects.filter(
            books__id__in=user_books
        ).annotate(
            freq=Count('id')
        ).order_by(
            '-freq'
        )[:5]

        tag_books = Book.objects.filter(
            tags__in=preferred_tags,
            status="approved"
        ).exclude(
            id__in=user_books
        )

        final_books = Book.objects.filter(
            Q(id__in=collaborative_ids)
            |
            Q(id__in=tag_books)
        ).distinct()[:10]

        return final_books

#搜索
class SearchView(APIView):

    def get(self, request):

        keyword = request.GET.get(
            "keyword",
            ""
        )

        tag = request.GET.get(
            "tag"
        )

        author = request.GET.get(
            "author"
        )

        min_rating = request.GET.get(
            "min_rating"
        )

        ordering = request.GET.get(
            "ordering"
        )

        page = int(
            request.GET.get(
                "page",
                1
            )
        )

        books = Book.objects.filter(
            status="approved"
        )

        if keyword:

            books = books.filter(
                Q(title__icontains=keyword)
                |
                Q(author__icontains=keyword)
                |
                Q(tags__name__icontains=keyword)
            )

        if tag:

            books = books.filter(
                tags__name=tag
            )

        if author:

            books = books.filter(
                author__icontains=author
            )

        if min_rating:

            books = books.filter(
                average_rating__gte=min_rating
            )

        if ordering == "latest":

            books = books.order_by(
                "-created_at"
            )

        elif ordering == "rating":

            books = books.order_by(
                "-average_rating"
            )

        elif ordering == "hot":

            books = books.order_by(
                "-likes_count",
                "-favorites_count"
            )

        paginator = Paginator(
            books.distinct(),
            10
        )

        page_obj = paginator.get_page(
            page
        )

        serializer = BookSerializer(
            page_obj.object_list,
            many=True
        )

        return Response({
            "count": paginator.count,
            "current_page": page,
            "filters": {
                "keyword": keyword,
                "tag": tag,
                "author": author,
                "min_rating": min_rating,
                "ordering": ordering
            },
            "results": serializer.data
        })

#书籍详情
class BookViewSet(viewsets.ModelViewSet):

    queryset = Book.objects.all()

    serializer_class = BookSerializer

    def perform_create(self, serializer):
        serializer.save(
            uploaded_by=self.request.user
        )

    def get_queryset(self):

        queryset = Book.objects.all()

        if not (
                self.request.user.is_authenticated
                and
                self.request.user.is_staff
        ):
            queryset = queryset.filter(
                status="approved"
            )

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

    def perform_create(
            self,
            serializer
    ):

        serializer.save(
            uploaded_by=self.request.user,
            status="pending"
        )

    def update(
            self,
            request,
            *args,
            **kwargs
    ):

        book = self.get_object()

        if (
                book.uploaded_by != request.user
                and
                not request.user.is_staff
        ):
            return Response(
                {
                    "error": "Permission denied"
                },
                status=403
            )

        return super().update(
            request,
            *args,
            **kwargs
        )

    def destroy(
            self,
            request,
            *args,
            **kwargs
    ):

        book = self.get_object()

        if (
                book.uploaded_by != request.user
                and
                not request.user.is_staff
        ):
            return Response(
                {
                    "error": "Permission denied"
                },
                status=403
            )

        return super().destroy(
            request,
            *args,
            **kwargs
        )


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

# 标签云接口
class TagCloudView(APIView):

    def get(self, request):

        tags = Tag.objects.annotate(
            book_count=Count("books")
        ).order_by(
            "-book_count"
        )

        data = []

        for tag in tags:

            data.append({
                "id": tag.id,
                "name": tag.name,
                "count": tag.book_count
            })

        return Response(data)

# 标签聚合页（注：后面前端用不上就删掉）
class TagBooksView(APIView):

    def get(self, request, tag_id):

        books = Book.objects.filter(
            tags__id=tag_id,
            status="approved"
        )

        serializer = BookSerializer(
            books,
            many=True
        )

        return Response(
            serializer.data
        )