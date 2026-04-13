from django.contrib import admin

from apps.catalog.models import Author, Book, Genre


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("name", "country", "birth_year", "death_year", "updated_at")
    search_fields = ("name", "country")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("name", "updated_at")
    search_fields = ("name",)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "publication_year",
        "language",
        "average_external_rating",
        "external_rating_count",
        "updated_at",
    )
    search_fields = ("title", "subtitle", "isbn10", "isbn13", "google_volume_id")
    list_filter = ("language", "source_name", "genres")
    filter_horizontal = ("authors", "genres")

# Register your models here.
