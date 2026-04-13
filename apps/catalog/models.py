from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Author(TimestampedModel):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=128, blank=True)
    birth_year = models.PositiveIntegerField(null=True, blank=True)
    death_year = models.PositiveIntegerField(null=True, blank=True)
    bio = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Genre(TimestampedModel):
    name = models.CharField(max_length=128, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


class Book(TimestampedModel):
    google_volume_id = models.CharField(max_length=128, unique=True, blank=True, null=True)
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    isbn10 = models.CharField(max_length=20, blank=True)
    isbn13 = models.CharField(max_length=20, blank=True)
    publication_year = models.PositiveIntegerField(null=True, blank=True)
    published_date_raw = models.CharField(max_length=32, blank=True)
    language = models.CharField(max_length=16, blank=True)
    page_count = models.PositiveIntegerField(null=True, blank=True)
    description = models.TextField(blank=True)
    cover_url = models.URLField(max_length=500, blank=True)
    preview_link = models.URLField(max_length=500, blank=True)
    info_link = models.URLField(max_length=500, blank=True)
    publisher = models.CharField(max_length=255, blank=True)
    average_external_rating = models.FloatField(
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(5)],
    )
    external_rating_count = models.PositiveIntegerField(default=0)
    source_name = models.CharField(max_length=64, default="google_books")
    source_url = models.URLField(max_length=500, blank=True)
    authors = models.ManyToManyField(Author, related_name="books", blank=True)
    genres = models.ManyToManyField(Genre, related_name="books", blank=True)

    class Meta:
        ordering = ("title",)

    def __str__(self):
        return self.title
