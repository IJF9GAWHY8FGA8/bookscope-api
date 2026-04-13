from django.db.models import Count
from rest_framework import permissions, viewsets

from apps.catalog.filters import BookFilter
from apps.catalog.models import Author, Book, Genre
from apps.catalog.serializers import AuthorSerializer, BookSerializer, GenreSerializer
from apps.catalog.services import annotate_books_queryset


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)


class BookViewSet(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    permission_classes = [IsAdminOrReadOnly]
    filterset_class = BookFilter
    search_fields = (
        "title",
        "subtitle",
        "description",
        "publisher",
        "authors__name",
        "genres__name",
        "isbn10",
        "isbn13",
    )
    ordering_fields = (
        "title",
        "publication_year",
        "average_external_rating",
        "external_rating_count",
        "local_average_rating",
        "popularity_score",
    )
    ordering = ("title",)

    def get_queryset(self):
        queryset = Book.objects.prefetch_related("authors", "genres")
        return annotate_books_queryset(queryset)


class AuthorViewSet(viewsets.ModelViewSet):
    serializer_class = AuthorSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ("name", "country")
    ordering_fields = ("name", "birth_year", "death_year", "books_count")
    ordering = ("name",)

    def get_queryset(self):
        return Author.objects.annotate(books_count=Count("books", distinct=True))


class GenreViewSet(viewsets.ModelViewSet):
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    search_fields = ("name",)
    ordering_fields = ("name", "books_count")
    ordering = ("name",)

    def get_queryset(self):
        return Genre.objects.annotate(books_count=Count("books", distinct=True))
