from rest_framework import serializers

from apps.catalog.models import Book
from apps.catalog.serializers import BookCompactSerializer
from apps.engagement.models import BookshelfEntry, Review


class BookshelfEntrySerializer(serializers.ModelSerializer):
    book = BookCompactSerializer(read_only=True)
    book_id = serializers.PrimaryKeyRelatedField(
        queryset=Book.objects.all(),
        source="book",
        write_only=True,
    )

    class Meta:
        model = BookshelfEntry
        fields = (
            "id",
            "book",
            "book_id",
            "status",
            "personal_rating",
            "is_favorite",
            "notes",
            "started_at",
            "finished_at",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        request = self.context["request"]
        book = attrs.get("book") or getattr(self.instance, "book", None)
        if book:
            queryset = BookshelfEntry.objects.filter(user=request.user, book=book)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    {"book_id": ["You already have a bookshelf entry for this book."]}
                )

        started_at = attrs.get("started_at") or getattr(self.instance, "started_at", None)
        finished_at = attrs.get("finished_at") or getattr(self.instance, "finished_at", None)
        if started_at and finished_at and finished_at < started_at:
            raise serializers.ValidationError(
                {"finished_at": ["Finished date cannot be earlier than started date."]}
            )
        return attrs


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = (
            "id",
            "username",
            "rating",
            "title",
            "content",
            "contains_spoiler",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        request = self.context["request"]
        book = self.context.get("book") or getattr(self.instance, "book", None)
        if request and request.user and request.user.is_authenticated and book:
            queryset = Review.objects.filter(user=request.user, book=book)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    {"book": ["You have already submitted a review for this book."]}
                )
        return attrs
