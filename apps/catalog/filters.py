import django_filters

from apps.catalog.models import Book


class BookFilter(django_filters.FilterSet):
    genre = django_filters.NumberFilter(field_name="genres__id")
    author = django_filters.NumberFilter(field_name="authors__id")
    language = django_filters.CharFilter(field_name="language", lookup_expr="iexact")
    year_min = django_filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="publication_year", lookup_expr="lte")

    class Meta:
        model = Book
        fields = ("genre", "author", "language", "year_min", "year_max")
