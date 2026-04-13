from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, viewsets

from apps.catalog.models import Book
from apps.engagement.models import BookshelfEntry, Review
from apps.engagement.serializers import BookshelfEntrySerializer, ReviewSerializer


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class BookshelfEntryViewSet(viewsets.ModelViewSet):
    queryset = BookshelfEntry.objects.none()
    serializer_class = BookshelfEntrySerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ("status", "is_favorite")
    ordering_fields = ("created_at", "updated_at", "personal_rating", "started_at", "finished_at")
    ordering = ("-updated_at",)

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False) or not self.request.user.is_authenticated:
            return BookshelfEntry.objects.none()
        return (
            BookshelfEntry.objects.filter(user=self.request.user)
            .select_related("book")
            .prefetch_related("book__authors", "book__genres")
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    queryset = Review.objects.none()

    def get_permissions(self):
        if self.request.method == "POST":
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs["book_id"]).select_related("user")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["book"] = get_object_or_404(Book, pk=self.kwargs["book_id"])
        return context

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, book=self.get_serializer_context()["book"])


class ReviewDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    queryset = Review.objects.select_related("user", "book")

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["book"] = self.get_object().book
        return context
