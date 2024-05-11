from django.urls import path, include

from rest_framework.routers import DefaultRouter
from .views import URLViewSet

router = DefaultRouter()
router.register(r'urls', URLViewSet)

urlpatterns = [
    path('api/', include(router.urls)), 
    path('<str:short_url>/', URLViewSet.as_view({'get': 'redirect'}), name='redirect'),
    ]