# BookScope API

BookScope API is a Django REST Framework project for book discovery, personal bookshelves, reviews, explainable recommendations, and reading analytics.

Public repository: <https://github.com/IJF9GAWHY8FGA8/bookscope-api>
Live deployment: <https://pw123.pythonanywhere.com/>

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

## Submission Deliverables

- [API documentation source](docs/api_documentation.md)
- [API documentation PDF](docs/api_documentation.pdf)
- [OpenAPI schema](docs/api_openapi.yaml)
- [Technical report source](docs/technical_report.md)
- [Technical report PDF](docs/technical_report.pdf)
- [GenAI appendix source](docs/genai_usage_appendix.md)
- [GenAI appendix PDF](docs/genai_usage_appendix.pdf)
- [Conversation logs appendix source](docs/conversation_logs_appendix.md)
- [Conversation logs appendix PDF](docs/conversation_logs_appendix.pdf)
- [PythonAnywhere deployment guide](docs/pythonanywhere_deployment.md)
- [Presentation outline](slides/bookscope_presentation_outline.md)
- [Presentation deck](slides/bookscope_presentation.pptx)

## API Documentation

Runtime schema endpoints:

- `/api/schema/`
- `/api/docs/`
- Live health check: `https://pw123.pythonanywhere.com/api/health/`
- Live Swagger UI: `https://pw123.pythonanywhere.com/api/docs/`

Generated submission assets:

- [OpenAPI schema](docs/api_openapi.yaml)
- [API documentation PDF](docs/api_documentation.pdf)
- [Technical report PDF](docs/technical_report.pdf)
- [GenAI appendix PDF](docs/genai_usage_appendix.pdf)
- [Conversation logs appendix PDF](docs/conversation_logs_appendix.pdf)
- [Presentation deck](slides/bookscope_presentation.pptx)

To rebuild the exported documentation assets:

```bash
python manage.py spectacular --file docs/api_openapi.yaml
python scripts/build_submission_assets.py
```

## Live Deployment

The project is deployed on PythonAnywhere:

- Live site: `https://pw123.pythonanywhere.com/`
- Health endpoint: `https://pw123.pythonanywhere.com/api/health/`
- Swagger UI: `https://pw123.pythonanywhere.com/api/docs/`
- Admin site: `https://pw123.pythonanywhere.com/admin/`
- Admin username: `pw123`
- Admin password: `QAZ1992519QAZ`

The repository also includes the deployment materials used for that release:

- [PythonAnywhere deployment guide](docs/pythonanywhere_deployment.md)
- [PythonAnywhere WSGI template](deployment/pythonanywhere_wsgi.py)
- Environment example in [.env.example](.env.example)

PythonAnywhere's official process uses:

- a manually configured web app
- a matching virtualenv
- the platform-side WSGI file from the `Web` tab
- static file mappings for `/static/` and optionally `/media/`

The hosted instance was verified after deployment with live checks against the health endpoint, Swagger UI, catalog listing, JWT authentication, bookshelf creation, review creation, and recommendation endpoints.

## Main Endpoint Groups

- Health and documentation: `/api/health/`, `/api/schema/`, `/api/docs/`
- Authentication: `/api/auth/`
- Catalog: `/api/books/`, `/api/authors/`, `/api/genres/`
- Personal bookshelf: `/api/me/bookshelf/`
- Reviews: `/api/books/{id}/reviews/`, `/api/reviews/{id}/`
- Recommendations: `/api/recommendations/`
- Analytics: `/api/analytics/`
