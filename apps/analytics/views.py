from rest_framework import permissions
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from apps.analytics.serializers import (
    GenrePopularityResponseSerializer,
    RatingsDistributionResponseSerializer,
    ReadingSummarySerializer,
    RecommendationResponseSerializer,
    SimpleBookAnalyticsResponseSerializer,
    TopAuthorResponseSerializer,
)
from apps.analytics.services import (
    get_genre_popularity,
    get_ratings_distribution,
    get_reading_summary,
    get_recommendations_for_user,
    get_similar_books,
    get_top_authors,
    get_trending_books,
)


class RecommendationForMeAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RecommendationResponseSerializer

    def get(self, request, *args, **kwargs):
        payload = {"results": get_recommendations_for_user(request.user)}
        return Response(self.get_serializer(payload).data)


class SimilarBooksAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SimpleBookAnalyticsResponseSerializer

    def get(self, request, book_id, *args, **kwargs):
        payload = {"results": get_similar_books(book_id)}
        return Response(self.get_serializer(payload).data)


class TrendingBooksAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = SimpleBookAnalyticsResponseSerializer

    def get(self, request, *args, **kwargs):
        payload = {"results": get_trending_books()}
        return Response(self.get_serializer(payload).data)


class GenrePopularityAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = GenrePopularityResponseSerializer

    def get(self, request, *args, **kwargs):
        payload = {"results": get_genre_popularity()}
        return Response(self.get_serializer(payload).data)


class RatingsDistributionAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RatingsDistributionResponseSerializer

    def get(self, request, *args, **kwargs):
        payload = {"results": get_ratings_distribution()}
        return Response(self.get_serializer(payload).data)


class ReadingSummaryAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ReadingSummarySerializer

    def get(self, request, *args, **kwargs):
        return Response(self.get_serializer(get_reading_summary(request.user)).data)


class TopAuthorsAPIView(GenericAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = TopAuthorResponseSerializer

    def get(self, request, *args, **kwargs):
        payload = {"results": get_top_authors()}
        return Response(self.get_serializer(payload).data)
