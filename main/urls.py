from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import URLViewSet

# Register the ViewSet with a router
router = DefaultRouter()
router.register(r"urls", URLViewSet, basename="url")

urlpatterns = [
    # API Endpoints
    path("api/", include(router.urls)),  # API routes for CRUD operations
    # Redirect Endpoint
    path("<str:short_url>/", URLViewSet.as_view({"get": "redirect"}), name="redirect"),
]
