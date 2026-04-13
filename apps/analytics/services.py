from collections import Counter
from datetime import timedelta
from typing import Dict, List

from django.db.models import Avg, Count, Q, Value
from django.db.models.functions import Coalesce
from django.utils import timezone

from apps.catalog.models import Book, Genre
from apps.catalog.services import annotate_books_queryset
from apps.engagement.models import BookshelfEntry, Review


def _build_preference_profile(user) -> Dict[str, Counter]:
    author_weights: Counter = Counter()
    genre_weights: Counter = Counter()

    bookshelf_entries = (
        BookshelfEntry.objects.filter(user=user)
        .exclude(personal_rating__isnull=True)
        .select_related("book")
        .prefetch_related("book__authors", "book__genres")
    )
    for entry in bookshelf_entries:
        if (entry.personal_rating or 0) < 4:
            continue
        weight = entry.personal_rating or 4
        for author in entry.book.authors.all():
            author_weights[author.id] += weight
        for genre in entry.book.genres.all():
            genre_weights[genre.id] += weight

    reviews = (
        Review.objects.filter(user=user, rating__gte=4)
        .select_related("book")
        .prefetch_related("book__authors", "book__genres")
    )
    for review in reviews:
        for author in review.book.authors.all():
            author_weights[author.id] += review.rating
        for genre in review.book.genres.all():
            genre_weights[genre.id] += review.rating

    return {"authors": author_weights, "genres": genre_weights}


def get_recommendations_for_user(user, limit: int = 10) -> List[dict]:
    excluded_book_ids = set(
        BookshelfEntry.objects.filter(user=user).values_list("book_id", flat=True)
    ) | set(Review.objects.filter(user=user).values_list("book_id", flat=True))

    queryset = annotate_books_queryset(
        Book.objects.exclude(id__in=excluded_book_ids).prefetch_related("authors", "genres")
    )
    profile = _build_preference_profile(user)
    author_weights = profile["authors"]
    genre_weights = profile["genres"]

    if not author_weights and not genre_weights:
        fallback = queryset.order_by(
            "-average_external_rating",
            "-external_rating_count",
            "-popularity_score",
            "title",
        )[:limit]
        return [
            {
                "book_id": book.id,
                "title": book.title,
                "cover_url": book.cover_url,
                "recommendation_score": round(
                    ((book.average_external_rating or 0) / 5) * 0.7
                    + min((book.external_rating_count or 0) / 1000, 1) * 0.3,
                    4,
                ),
                "reasons": [
                    "Popular fallback recommendation based on catalog rating and community activity."
                ],
                "authors": [author.name for author in book.authors.all()],
                "genres": [genre.name for genre in book.genres.all()],
            }
            for book in fallback
        ]

    max_author_weight = max(author_weights.values(), default=1)
    max_genre_weight = max(genre_weights.values(), default=1)
    scored_results = []

    for book in queryset:
        author_match = (
            sum(author_weights.get(author.id, 0) for author in book.authors.all()) / max_author_weight
            if max_author_weight
            else 0
        )
        genre_match = (
            sum(genre_weights.get(genre.id, 0) for genre in book.genres.all()) / max_genre_weight
            if max_genre_weight
            else 0
        )
        external_rating_score = (book.average_external_rating or 0) / 5
        external_count_score = min((book.external_rating_count or 0) / 1000, 1)
        popularity_score = min((getattr(book, "popularity_score", 0) or 0) / 25, 1)

        recommendation_score = (
            0.35 * min(genre_match, 1)
            + 0.25 * min(author_match, 1)
            + 0.2 * external_rating_score
            + 0.1 * external_count_score
            + 0.1 * popularity_score
        )

        reasons = []
        matched_genres = [genre.name for genre in book.genres.all() if genre_weights.get(genre.id)]
        matched_authors = [author.name for author in book.authors.all() if author_weights.get(author.id)]
        if matched_genres:
            reasons.append(f"Matches your preferred genres: {', '.join(matched_genres[:3])}")
        if matched_authors:
            reasons.append(f"Includes authors similar to books you rated highly: {', '.join(matched_authors[:2])}")
        if book.average_external_rating:
            reasons.append("Has a strong external community rating.")

        scored_results.append(
            {
                "book_id": book.id,
                "title": book.title,
                "cover_url": book.cover_url,
                "recommendation_score": round(recommendation_score, 4),
                "reasons": reasons or ["Recommended from your reading profile."],
                "authors": [author.name for author in book.authors.all()],
                "genres": [genre.name for genre in book.genres.all()],
            }
        )

    return sorted(
        scored_results,
        key=lambda item: (-item["recommendation_score"], item["title"].lower()),
    )[:limit]


def get_similar_books(book_id: int, limit: int = 10) -> List[dict]:
    book = Book.objects.prefetch_related("authors", "genres").get(pk=book_id)
    source_author_ids = {author.id for author in book.authors.all()}
    source_genre_ids = {genre.id for genre in book.genres.all()}

    queryset = annotate_books_queryset(
        Book.objects.exclude(pk=book.pk).prefetch_related("authors", "genres")
    )

    scored_results = []
    for candidate in queryset:
        shared_authors = source_author_ids & {author.id for author in candidate.authors.all()}
        shared_genres = source_genre_ids & {genre.id for genre in candidate.genres.all()}
        if not shared_authors and not shared_genres:
            continue

        score = (len(shared_genres) * 0.6) + (len(shared_authors) * 0.4)
        score += ((candidate.average_external_rating or 0) / 5) * 0.2
        scored_results.append(
            {
                "book_id": candidate.id,
                "title": candidate.title,
                "cover_url": candidate.cover_url,
                "score": round(score, 4),
            }
        )

    return sorted(scored_results, key=lambda item: (-item["score"], item["title"].lower()))[:limit]


def get_trending_books(limit: int = 10) -> List[dict]:
    recent_window = timezone.now() - timedelta(days=30)
    queryset = annotate_books_queryset(Book.objects.prefetch_related("authors", "genres")).annotate(
        recent_bookshelf_count=Count(
            "bookshelf_entries",
            filter=Q(bookshelf_entries__created_at__gte=recent_window),
            distinct=True,
        ),
        recent_review_count=Count(
            "reviews",
            filter=Q(reviews__created_at__gte=recent_window),
            distinct=True,
        ),
    )

    results = []
    for book in queryset:
        score = (
            (book.recent_bookshelf_count or 0)
            + (book.recent_review_count or 0) * 1.5
            + ((book.average_external_rating or 0) / 5)
        )
        results.append(
            {
                "book_id": book.id,
                "title": book.title,
                "cover_url": book.cover_url,
                "score": round(score, 4),
            }
        )
    return sorted(results, key=lambda item: (-item["score"], item["title"].lower()))[:limit]


def get_genre_popularity(limit: int = 10) -> List[dict]:
    genres = (
        Genre.objects.annotate(
            bookshelf_count=Count("books__bookshelf_entries", distinct=True),
            review_count=Count("books__reviews", distinct=True),
            average_rating=Coalesce(Avg("books__reviews__rating"), Value(0.0)),
        )
        .order_by("-bookshelf_count", "-review_count", "name")[:limit]
    )
    return [
        {
            "genre_id": genre.id,
            "genre_name": genre.name,
            "bookshelf_count": genre.bookshelf_count,
            "review_count": genre.review_count,
            "average_rating": round(float(genre.average_rating or 0), 2),
        }
        for genre in genres
    ]


def get_ratings_distribution() -> List[dict]:
    distribution = Review.objects.values("rating").annotate(count=Count("id")).order_by("rating")
    return [{"rating": item["rating"], "count": item["count"]} for item in distribution]


def get_reading_summary(user) -> dict:
    queryset = BookshelfEntry.objects.filter(user=user).select_related("book").prefetch_related("book__genres")
    status_counts = Counter(queryset.values_list("status", flat=True))
    favorite_count = queryset.filter(is_favorite=True).count()
    avg_rating = queryset.exclude(personal_rating__isnull=True).aggregate(avg=Avg("personal_rating"))["avg"] or 0

    genre_counts: Counter = Counter()
    for entry in queryset:
        for genre in entry.book.genres.all():
            genre_counts[genre.name] += 1

    return {
        "total_entries": queryset.count(),
        "want_to_read": status_counts.get(BookshelfEntry.Status.WANT_TO_READ, 0),
        "reading": status_counts.get(BookshelfEntry.Status.READING, 0),
        "completed": status_counts.get(BookshelfEntry.Status.COMPLETED, 0),
        "dropped": status_counts.get(BookshelfEntry.Status.DROPPED, 0),
        "favorites": favorite_count,
        "average_personal_rating": round(float(avg_rating), 2),
        "top_genres": [name for name, _ in genre_counts.most_common(3)],
    }


def get_top_authors(limit: int = 10) -> List[dict]:
    authors = (
        Book.authors.through.objects.values("author_id", "author__name")
        .annotate(
            bookshelf_count=Count("book__bookshelf_entries", distinct=True),
            review_count=Count("book__reviews", distinct=True),
            average_rating=Coalesce(Avg("book__reviews__rating"), Value(0.0)),
        )
        .order_by("-bookshelf_count", "-review_count", "author__name")[:limit]
    )
    return [
        {
            "author_id": item["author_id"],
            "author_name": item["author__name"],
            "bookshelf_count": item["bookshelf_count"],
            "review_count": item["review_count"],
            "average_rating": round(float(item["average_rating"] or 0), 2),
        }
        for item in authors
    ]
