# BookScope API Documentation

## Overview

BookScope API is a REST API for book catalog browsing, personal bookshelf management, reviews, explainable recommendations, and reading analytics.

## Authentication

Authentication uses Bearer tokens via JSON Web Tokens.

### Register

- `POST /api/auth/register/`

Example request:

```json
{
  "username": "reader1",
  "email": "reader1@example.com",
  "password": "StrongPass123!"
}
```

### Obtain Access Token

- `POST /api/auth/token/`

Example request:

```json
{
  "username": "reader1",
  "password": "StrongPass123!"
}
```

### Refresh Token

- `POST /api/auth/token/refresh/`

### Current User

- `GET /api/auth/me/`

Requires:

- `Authorization: Bearer <access-token>`

## Catalog Endpoints

### Books

- `GET /api/books/`
- `POST /api/books/`
- `GET /api/books/{id}/`
- `PATCH /api/books/{id}/`
- `DELETE /api/books/{id}/`

Supported list query parameters:

- `search`
- `genre`
- `author`
- `language`
- `year_min`
- `year_max`
- `ordering`
- `page`
- `page_size`

### Authors

- `GET /api/authors/`
- `POST /api/authors/`
- `GET /api/authors/{id}/`
- `PATCH /api/authors/{id}/`
- `DELETE /api/authors/{id}/`

### Genres

- `GET /api/genres/`
- `POST /api/genres/`
- `GET /api/genres/{id}/`
- `PATCH /api/genres/{id}/`
- `DELETE /api/genres/{id}/`

## Bookshelf Endpoints

These endpoints require authentication.

- `GET /api/me/bookshelf/`
- `POST /api/me/bookshelf/`
- `GET /api/me/bookshelf/{id}/`
- `PATCH /api/me/bookshelf/{id}/`
- `DELETE /api/me/bookshelf/{id}/`

Example request:

```json
{
  "book_id": 1,
  "status": "reading",
  "personal_rating": 5,
  "is_favorite": true,
  "notes": "Strong first impression."
}
```

## Review Endpoints

- `GET /api/books/{id}/reviews/`
- `POST /api/books/{id}/reviews/`
- `PATCH /api/reviews/{id}/`
- `DELETE /api/reviews/{id}/`

Example request:

```json
{
  "rating": 5,
  "title": "Excellent",
  "content": "Focused, practical, and easy to apply.",
  "contains_spoiler": false
}
```

## Recommendation Endpoints

### Personalized Recommendations

- `GET /api/recommendations/for-me/`

Behavior:

- uses personal bookshelf ratings and review ratings
- excludes books already present in the user's bookshelf or review history
- returns human-readable recommendation reasons

### Similar Books

- `GET /api/recommendations/similar-books/{book_id}/`

## Analytics Endpoints

- `GET /api/analytics/books/trending/`
- `GET /api/analytics/genres/popularity/`
- `GET /api/analytics/ratings/distribution/`
- `GET /api/analytics/me/reading-summary/`
- `GET /api/analytics/authors/top/`

## Error Handling

The API returns structured JSON errors.

Example response:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Validation failed.",
    "details": {
      "book_id": [
        "You already have a bookshelf entry for this book."
      ]
    }
  }
}
```

## Status Code Conventions

- `200 OK`
- `201 Created`
- `204 No Content`
- `400 Bad Request`
- `401 Unauthorized`
- `403 Forbidden`
- `404 Not Found`

## Google Books Data Import

The catalog is designed to ingest Google Books metadata into the local SQLite database.

Typical workflow:

1. Fetch Google Books payloads.
2. Normalize titles, authors, genres, ISBNs, and metadata.
3. Store them in local tables.
4. Build recommendations and analytics from local data plus user activity.

## OpenAPI Schema

The machine-readable schema is exported to `docs/api_openapi.yaml`.
