from django.contrib import admin

from apps.engagement.models import BookshelfEntry, Review


@admin.register(BookshelfEntry)
class BookshelfEntryAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "status", "personal_rating", "is_favorite", "updated_at")
    list_filter = ("status", "is_favorite")
    search_fields = ("user__username", "book__title")


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "rating", "contains_spoiler", "created_at")
    list_filter = ("rating", "contains_spoiler")
    search_fields = ("user__username", "book__title", "title")

# Register your models here.
