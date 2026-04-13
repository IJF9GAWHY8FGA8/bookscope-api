from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from apps.catalog.models import TimestampedModel


class BookshelfEntry(TimestampedModel):
    class Status(models.TextChoices):
        WANT_TO_READ = "want_to_read", "Want to Read"
        READING = "reading", "Reading"
        COMPLETED = "completed", "Completed"
        DROPPED = "dropped", "Dropped"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="bookshelf_entries",
    )
    book = models.ForeignKey(
        "catalog.Book",
        on_delete=models.CASCADE,
        related_name="bookshelf_entries",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.WANT_TO_READ,
    )
    personal_rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
    )
    is_favorite = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    started_at = models.DateField(null=True, blank=True)
    finished_at = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ("-updated_at",)
        constraints = [
            models.UniqueConstraint(fields=("user", "book"), name="unique_bookshelf_entry_per_user"),
        ]

    def __str__(self):
        return f"{self.user} -> {self.book} ({self.status})"


class Review(TimestampedModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    book = models.ForeignKey(
        "catalog.Book",
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=255, blank=True)
    content = models.TextField()
    contains_spoiler = models.BooleanField(default=False)

    class Meta:
        ordering = ("-created_at",)
        constraints = [
            models.UniqueConstraint(fields=("user", "book"), name="unique_review_per_user_book"),
        ]

    def __str__(self):
        return f"Review({self.user}, {self.book}, {self.rating})"
