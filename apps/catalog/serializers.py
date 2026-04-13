from rest_framework import serializers

from apps.catalog.models import Author, Book, Genre


class AuthorSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Author
        fields = (
            "id",
            "name",
            "country",
            "birth_year",
            "death_year",
            "bio",
            "books_count",
            "created_at",
            "updated_at",
        )


class GenreSerializer(serializers.ModelSerializer):
    books_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Genre
        fields = (
            "id",
            "name",
            "description",
            "books_count",
            "created_at",
            "updated_at",
        )


class AuthorSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ("id", "name")


class GenreSummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ("id", "name")


class BookCompactSerializer(serializers.ModelSerializer):
    authors = AuthorSummarySerializer(many=True, read_only=True)
    genres = GenreSummarySerializer(many=True, read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "title",
            "subtitle",
            "cover_url",
            "publication_year",
            "language",
            "average_external_rating",
            "external_rating_count",
            "authors",
            "genres",
        )


class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSummarySerializer(many=True, read_only=True)
    genres = GenreSummarySerializer(many=True, read_only=True)
    author_ids = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(),
        many=True,
        source="authors",
        write_only=True,
        required=False,
    )
    genre_ids = serializers.PrimaryKeyRelatedField(
        queryset=Genre.objects.all(),
        many=True,
        source="genres",
        write_only=True,
        required=False,
    )
    local_average_rating = serializers.FloatField(read_only=True)
    local_review_count = serializers.IntegerField(read_only=True)
    bookshelf_count = serializers.IntegerField(read_only=True)
    popularity_score = serializers.IntegerField(read_only=True)

    class Meta:
        model = Book
        fields = (
            "id",
            "google_volume_id",
            "title",
            "subtitle",
            "isbn10",
            "isbn13",
            "publication_year",
            "published_date_raw",
            "language",
            "page_count",
            "description",
            "cover_url",
            "preview_link",
            "info_link",
            "publisher",
            "average_external_rating",
            "external_rating_count",
            "source_name",
            "source_url",
            "authors",
            "genres",
            "author_ids",
            "genre_ids",
            "local_average_rating",
            "local_review_count",
            "bookshelf_count",
            "popularity_score",
            "created_at",
            "updated_at",
        )
