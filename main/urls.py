from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import URLViewSet
from django.conf import settings
from django.conf.urls.static import static

# Register the ViewSet with a router
router = DefaultRouter()
router.register(r"urls", URLViewSet, basename="url")

urlpatterns = [
    # API Endpoints
    path("api/", include(router.urls)),  # API routes for CRUD operations
    # Redirect Endpoint
    path("<str:short_url>/", URLViewSet.as_view({"get": "redirect"}), name="redirect"),
    # Analytics Endpoint
    path(
        "api/urls/<str:pk>/analytics/",
        URLViewSet.as_view({"get": "analytics"}),
        name="url-analytics",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
