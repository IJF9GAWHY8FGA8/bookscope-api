from django.urls import path

from apps.analytics.views import (
    GenrePopularityAPIView,
    RatingsDistributionAPIView,
    ReadingSummaryAPIView,
    RecommendationForMeAPIView,
    SimilarBooksAPIView,
    TopAuthorsAPIView,
    TrendingBooksAPIView,
)

urlpatterns = [
    path("recommendations/for-me/", RecommendationForMeAPIView.as_view(), name="recommendations-for-me"),
    path(
        "recommendations/similar-books/<int:book_id>/",
        SimilarBooksAPIView.as_view(),
        name="similar-books",
    ),
    path("analytics/books/trending/", TrendingBooksAPIView.as_view(), name="analytics-trending-books"),
    path(
        "analytics/genres/popularity/",
        GenrePopularityAPIView.as_view(),
        name="analytics-genre-popularity",
    ),
    path(
        "analytics/ratings/distribution/",
        RatingsDistributionAPIView.as_view(),
        name="analytics-ratings-distribution",
    ),
    path(
        "analytics/me/reading-summary/",
        ReadingSummaryAPIView.as_view(),
        name="analytics-reading-summary",
    ),
    path("analytics/authors/top/", TopAuthorsAPIView.as_view(), name="analytics-top-authors"),
]
