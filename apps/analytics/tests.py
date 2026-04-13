from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Author, Book, Genre
from apps.engagement.models import BookshelfEntry, Review

User = get_user_model()


class AnalyticsAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reader2",
            email="reader2@example.com",
            password="StrongPass123!",
        )
        author = Author.objects.create(name="Author One")
        productivity = Genre.objects.create(name="Productivity")
        strategy = Genre.objects.create(name="Strategy")

        self.book_a = Book.objects.create(
            title="Focus Better",
            language="en",
            average_external_rating=4.4,
            external_rating_count=500,
        )
        self.book_a.authors.add(author)
        self.book_a.genres.add(productivity)

        self.book_b = Book.objects.create(
            title="Strategic Thinking",
            language="en",
            average_external_rating=4.8,
            external_rating_count=1200,
        )
        self.book_b.authors.add(author)
        self.book_b.genres.add(productivity, strategy)

        self.book_c = Book.objects.create(
            title="Creative Planning",
            language="en",
            average_external_rating=4.0,
            external_rating_count=300,
        )
        self.book_c.genres.add(strategy)

        BookshelfEntry.objects.create(
            user=self.user,
            book=self.book_a,
            status=BookshelfEntry.Status.COMPLETED,
            personal_rating=5,
            is_favorite=True,
        )
        Review.objects.create(
            user=self.user,
            book=self.book_a,
            rating=5,
            title="Useful",
            content="Very actionable.",
        )
        self.client.force_authenticate(self.user)

    def test_recommendations_exclude_existing_bookshelf_books(self):
        response = self.client.get("/api/recommendations/for-me/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        returned_ids = [item["book_id"] for item in response.data["results"]]
        self.assertNotIn(self.book_a.id, returned_ids)
        self.assertIn(self.book_b.id, returned_ids)

    def test_reading_summary_returns_user_stats(self):
        response = self.client.get("/api/analytics/me/reading-summary/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["completed"], 1)
        self.assertEqual(response.data["favorites"], 1)

    def test_genre_popularity_is_public(self):
        self.client.force_authenticate(user=None)
        response = self.client.get("/api/analytics/genres/popularity/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data["results"]), 1)
