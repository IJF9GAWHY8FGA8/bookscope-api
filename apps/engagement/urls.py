from rest_framework.routers import DefaultRouter
from django.urls import path

from apps.engagement.views import BookReviewListCreateAPIView, BookshelfEntryViewSet, ReviewDetailAPIView

router = DefaultRouter()
router.register(r"me/bookshelf", BookshelfEntryViewSet, basename="my-bookshelf")

urlpatterns = [
    path("books/<int:book_id>/reviews/", BookReviewListCreateAPIView.as_view(), name="book-reviews"),
    path("reviews/<int:pk>/", ReviewDetailAPIView.as_view(), name="review-detail"),
]

urlpatterns += router.urls
