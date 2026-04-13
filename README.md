# BookScope API

BookScope API is a Django REST Framework project for book discovery, personal bookshelves, reviews, explainable recommendations, and reading analytics.

## Core Features

- Google Books ingestion into a local SQLite-backed catalog
- Book, author, and genre management APIs
- Personal bookshelf tracking with reading states and notes
- Book reviews and rating aggregation
- Rule-based recommendations for signed-in users
- Aggregate analytics for genres, ratings, and reading activity
- OpenAPI schema generation via `drf-spectacular`

## Stack

- Python 3.8+
- Django 4.2
- Django REST Framework
- SQLite
- Simple JWT
- django-filter
- drf-spectacular

## Quick Start

1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` if you want to override defaults.
4. Run migrations with `python manage.py migrate`.
5. Create a superuser with `python manage.py createsuperuser`.
6. Import sample catalog data with `python manage.py import_google_books --input-file data/samples/google_books_raw_sample.json`.
7. Start the server with `python manage.py runserver`.

## Environment Variables

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `GOOGLE_BOOKS_API_KEY`

## Data Import

The catalog is designed to ingest Google Books payloads and normalize them into local tables for books, authors, and genres.

### Import from the bundled sample file

```bash
python manage.py import_google_books --input-file data/samples/google_books_raw_sample.json
```

### Import directly from Google Books

```bash
python manage.py import_google_books --query "productivity" --pages 2 --max-results 20
```

If you have an API key, place it in `.env` as `GOOGLE_BOOKS_API_KEY`.

## Testing

Run the test suite with:

```bash
pytest
```

## API Documentation

Runtime schema endpoints:

- `/api/schema/`
- `/api/docs/`

Generated submission assets:

- `docs/api_openapi.yaml`
- `docs/api_documentation.md`
- `docs/api_documentation.pdf`
- `docs/technical_report.md`
- `docs/technical_report.pdf`
- `docs/genai_usage_appendix.md`
- `docs/genai_usage_appendix.pdf`
- `slides/bookscope_presentation.pptx`

To rebuild the exported documentation assets:

```bash
python manage.py spectacular --file docs/api_openapi.yaml
python scripts/build_submission_assets.py
```

## Main Endpoint Groups

- Authentication: `/api/auth/`
- Catalog: `/api/books/`, `/api/authors/`, `/api/genres/`
- Personal bookshelf: `/api/me/bookshelf/`
- Reviews: `/api/books/{id}/reviews/`, `/api/reviews/{id}/`
- Recommendations: `/api/recommendations/`
- Analytics: `/api/analytics/`
