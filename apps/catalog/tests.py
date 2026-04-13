from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

from apps.catalog.models import Author, Book, Genre

User = get_user_model()


class CatalogAPITestCase(APITestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Cal Newport")
        self.genre = Genre.objects.create(name="Productivity")
        self.book = Book.objects.create(
            title="Deep Work",
            language="en",
            publication_year=2016,
            average_external_rating=4.5,
            external_rating_count=850,
        )
        self.book.authors.add(self.author)
        self.book.genres.add(self.genre)

        self.admin_user = User.objects.create_user(
            username="adminuser",
            email="admin@example.com",
            password="StrongPass123!",
            is_staff=True,
        )

    def test_public_book_list_supports_search(self):
        response = self.client.get("/api/books/?search=Deep")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["count"], 1)

    def test_admin_can_create_book(self):
        self.client.force_authenticate(self.admin_user)
        response = self.client.post(
            "/api/books/",
            {
                "title": "Digital Minimalism",
                "language": "en",
                "publication_year": 2019,
                "author_ids": [self.author.id],
                "genre_ids": [self.genre.id],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
