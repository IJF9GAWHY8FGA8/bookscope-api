import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path("/home/YOUR_PYTHONANYWHERE_USERNAME/bookscope-api")

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

load_dotenv(PROJECT_ROOT / ".env")

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bookscope.settings")
os.environ.setdefault("DJANGO_DEBUG", "False")
os.environ.setdefault(
    "DJANGO_ALLOWED_HOSTS",
    "YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com",
)
os.environ.setdefault(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    "https://YOUR_PYTHONANYWHERE_USERNAME.pythonanywhere.com",
)

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
