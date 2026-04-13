import json
import re
from pathlib import Path
from typing import Iterable, List, Optional

import requests
from django.conf import settings
from django.db.models import Avg, Count, F, QuerySet, Value
from django.db.models.functions import Coalesce

from apps.catalog.models import Author, Book, Genre

GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"


def annotate_books_queryset(queryset: QuerySet) -> QuerySet:
    queryset = queryset.annotate(
        local_average_rating=Coalesce(Avg("reviews__rating"), Value(0.0)),
        local_review_count=Count("reviews", distinct=True),
        bookshelf_count=Count("bookshelf_entries", distinct=True),
    )
    return queryset.annotate(popularity_score=F("local_review_count") + F("bookshelf_count"))


def _extract_identifier(identifiers: Iterable[dict], identifier_type: str) -> str:
    for identifier in identifiers or []:
        if identifier.get("type") == identifier_type:
            return str(identifier.get("identifier", "")).strip()
    return ""


def _parse_publication_year(raw_value: str) -> Optional[int]:
    if not raw_value:
        return None
    match = re.match(r"^(\d{4})", raw_value)
    return int(match.group(1)) if match else None


def normalize_google_books_item(item: dict) -> dict:
    volume_info = item.get("volumeInfo", {})
    image_links = volume_info.get("imageLinks", {})
    authors = [author.strip() for author in volume_info.get("authors", []) if author.strip()]
    genres = [genre.strip() for genre in volume_info.get("categories", []) if genre.strip()]
    published_date_raw = str(volume_info.get("publishedDate", "")).strip()

    return {
        "google_volume_id": item.get("id") or "",
        "title": str(volume_info.get("title", "")).strip(),
        "subtitle": str(volume_info.get("subtitle", "")).strip(),
        "isbn10": _extract_identifier(volume_info.get("industryIdentifiers", []), "ISBN_10"),
        "isbn13": _extract_identifier(volume_info.get("industryIdentifiers", []), "ISBN_13"),
        "publication_year": _parse_publication_year(published_date_raw),
        "published_date_raw": published_date_raw,
        "language": str(volume_info.get("language", "")).strip(),
        "page_count": volume_info.get("pageCount"),
        "description": str(volume_info.get("description", "")).strip(),
        "cover_url": image_links.get("thumbnail") or image_links.get("smallThumbnail") or "",
        "preview_link": str(volume_info.get("previewLink", "")).strip(),
        "info_link": str(volume_info.get("infoLink", "")).strip(),
        "publisher": str(volume_info.get("publisher", "")).strip(),
        "average_external_rating": volume_info.get("averageRating"),
        "external_rating_count": volume_info.get("ratingsCount") or 0,
        "source_name": "google_books",
        "source_url": f"{GOOGLE_BOOKS_API_URL}/{item.get('id', '')}".rstrip("/"),
        "authors": authors,
        "genres": genres,
    }


def fetch_google_books_page(
    *,
    query: str,
    start_index: int = 0,
    max_results: int = 20,
    lang_restrict: str = "",
    api_key: str = "",
) -> dict:
    params = {
        "q": query,
        "startIndex": start_index,
        "maxResults": max_results,
        "printType": "books",
    }
    if lang_restrict:
        params["langRestrict"] = lang_restrict
    if api_key:
        params["key"] = api_key

    response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_google_books_pages(
    *,
    query: str,
    pages: int = 1,
    max_results: int = 20,
    lang_restrict: str = "",
    api_key: str = "",
) -> List[dict]:
    payloads: List[dict] = []
    for page_number in range(pages):
        payload = fetch_google_books_page(
            query=query,
            start_index=page_number * max_results,
            max_results=max_results,
            lang_restrict=lang_restrict,
            api_key=api_key or settings.GOOGLE_BOOKS_API_KEY,
        )
        payloads.append(payload)
        if not payload.get("items"):
            break
    return payloads


def save_raw_payload(payload, output_file: str) -> None:
    path = Path(output_file)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True))


def load_payload_from_file(input_file: str):
    return json.loads(Path(input_file).read_text())


def import_google_books_payload(payload) -> int:
    payloads = payload if isinstance(payload, list) else [payload]
    imported = 0

    for page_payload in payloads:
        for item in page_payload.get("items", []):
            normalized = normalize_google_books_item(item)
            if not normalized["title"]:
                continue

            lookup = {}
            if normalized["google_volume_id"]:
                lookup["google_volume_id"] = normalized["google_volume_id"]
            elif normalized["isbn13"]:
                lookup["isbn13"] = normalized["isbn13"]
            else:
                lookup["title"] = normalized["title"]

            book, _ = Book.objects.update_or_create(
                **lookup,
                defaults={
                    "title": normalized["title"],
                    "subtitle": normalized["subtitle"],
                    "isbn10": normalized["isbn10"],
                    "isbn13": normalized["isbn13"],
                    "publication_year": normalized["publication_year"],
                    "published_date_raw": normalized["published_date_raw"],
                    "language": normalized["language"],
                    "page_count": normalized["page_count"],
                    "description": normalized["description"],
                    "cover_url": normalized["cover_url"],
                    "preview_link": normalized["preview_link"],
                    "info_link": normalized["info_link"],
                    "publisher": normalized["publisher"],
                    "average_external_rating": normalized["average_external_rating"],
                    "external_rating_count": normalized["external_rating_count"],
                    "source_name": normalized["source_name"],
                    "source_url": normalized["source_url"],
                },
            )

            author_objects = [
                Author.objects.get_or_create(name=author_name)[0]
                for author_name in normalized["authors"]
            ]
            genre_objects = [
                Genre.objects.get_or_create(name=genre_name)[0]
                for genre_name in normalized["genres"]
            ]

            if author_objects:
                book.authors.set(author_objects)
            if genre_objects:
                book.genres.set(genre_objects)

            imported += 1

    return imported
