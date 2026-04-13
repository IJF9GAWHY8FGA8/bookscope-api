from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from apps.catalog.services import (
    fetch_google_books_pages,
    import_google_books_payload,
    load_payload_from_file,
    save_raw_payload,
)


class Command(BaseCommand):
    help = "Import catalog data from Google Books into the local database."

    def add_arguments(self, parser):
        parser.add_argument("--query", type=str, default="")
        parser.add_argument("--lang", type=str, default="")
        parser.add_argument("--pages", type=int, default=1)
        parser.add_argument("--max-results", type=int, default=20)
        parser.add_argument("--api-key", type=str, default="")
        parser.add_argument("--input-file", type=str, default="")
        parser.add_argument("--output-file", type=str, default="")

    def handle(self, *args, **options):
        input_file = options["input_file"]

        if input_file:
            payload = load_payload_from_file(input_file)
        else:
            query = options["query"].strip()
            if not query:
                raise CommandError("Either --query or --input-file is required.")

            payload = fetch_google_books_pages(
                query=query,
                pages=options["pages"],
                max_results=options["max_results"],
                lang_restrict=options["lang"],
                api_key=options["api_key"] or settings.GOOGLE_BOOKS_API_KEY,
            )

            if options["output_file"]:
                save_raw_payload(payload, options["output_file"])

        imported = import_google_books_payload(payload)
        self.stdout.write(self.style.SUCCESS(f"Imported or updated {imported} books."))
