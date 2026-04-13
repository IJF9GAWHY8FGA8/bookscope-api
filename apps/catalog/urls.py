from rest_framework.routers import DefaultRouter

from apps.catalog.views import AuthorViewSet, BookViewSet, GenreViewSet

router = DefaultRouter()
router.register("books", BookViewSet, basename="books")
router.register("authors", AuthorViewSet, basename="authors")
router.register("genres", GenreViewSet, basename="genres")

urlpatterns = router.urls
