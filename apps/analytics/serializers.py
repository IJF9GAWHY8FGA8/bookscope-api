from rest_framework import serializers


class RecommendationItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    title = serializers.CharField()
    cover_url = serializers.CharField(allow_blank=True)
    recommendation_score = serializers.FloatField()
    reasons = serializers.ListField(child=serializers.CharField())
    authors = serializers.ListField(child=serializers.CharField())
    genres = serializers.ListField(child=serializers.CharField())


class SimpleBookAnalyticsSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()
    title = serializers.CharField()
    cover_url = serializers.CharField(allow_blank=True)
    score = serializers.FloatField()


class GenrePopularitySerializer(serializers.Serializer):
    genre_id = serializers.IntegerField()
    genre_name = serializers.CharField()
    bookshelf_count = serializers.IntegerField()
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()


class RatingsDistributionSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
    count = serializers.IntegerField()


class ReadingSummarySerializer(serializers.Serializer):
    total_entries = serializers.IntegerField()
    want_to_read = serializers.IntegerField()
    reading = serializers.IntegerField()
    completed = serializers.IntegerField()
    dropped = serializers.IntegerField()
    favorites = serializers.IntegerField()
    average_personal_rating = serializers.FloatField()
    top_genres = serializers.ListField(child=serializers.CharField())


class TopAuthorSerializer(serializers.Serializer):
    author_id = serializers.IntegerField()
    author_name = serializers.CharField()
    bookshelf_count = serializers.IntegerField()
    review_count = serializers.IntegerField()
    average_rating = serializers.FloatField()


class RecommendationResponseSerializer(serializers.Serializer):
    results = RecommendationItemSerializer(many=True)


class SimpleBookAnalyticsResponseSerializer(serializers.Serializer):
    results = SimpleBookAnalyticsSerializer(many=True)


class GenrePopularityResponseSerializer(serializers.Serializer):
    results = GenrePopularitySerializer(many=True)


class RatingsDistributionResponseSerializer(serializers.Serializer):
    results = RatingsDistributionSerializer(many=True)


class TopAuthorResponseSerializer(serializers.Serializer):
    results = TopAuthorSerializer(many=True)
