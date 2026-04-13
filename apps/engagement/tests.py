from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Author, Book, Genre
from apps.engagement.models import BookshelfEntry, Review

User = get_user_model()


class EngagementAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="reader",
            email="reader@example.com",
            password="StrongPass123!",
        )
        author = Author.objects.create(name="James Clear")
        genre = Genre.objects.create(name="Self Help")
        self.book = Book.objects.create(title="Atomic Habits", language="en")
        self.book.authors.add(author)
        self.book.genres.add(genre)
        self.client.force_authenticate(self.user)

    def test_user_can_manage_bookshelf_entries(self):
        create_response = self.client.post(
            "/api/me/bookshelf/",
            {
                "book_id": self.book.id,
                "status": "reading",
                "personal_rating": 5,
                "is_favorite": True,
            },
            format="json",
        )
        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(BookshelfEntry.objects.count(), 1)

        list_response = self.client.get("/api/me/bookshelf/")
        self.assertEqual(list_response.status_code, status.HTTP_200_OK)
        self.assertEqual(list_response.data["count"], 1)

    def test_duplicate_bookshelf_entries_are_rejected(self):
        BookshelfEntry.objects.create(user=self.user, book=self.book)
        response = self.client.post(
            "/api/me/bookshelf/",
            {"book_id": self.book.id, "status": "completed"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_can_only_create_one_review_per_book(self):
        first_review = self.client.post(
            f"/api/books/{self.book.id}/reviews/",
            {"rating": 5, "title": "Excellent", "content": "Great read.", "contains_spoiler": False},
            format="json",
        )
        self.assertEqual(first_review.status_code, status.HTTP_201_CREATED)

        second_review = self.client.post(
            f"/api/books/{self.book.id}/reviews/",
            {"rating": 4, "title": "Again", "content": "Still good.", "contains_spoiler": False},
            format="json",
        )
        self.assertEqual(second_review.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Review.objects.count(), 1)
