# Django imports
from django.shortcuts import redirect
from django.http import Http404, HttpResponseForbidden

# REST Framework imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Project file imports
from .models import URL
from .serializers import URLSerializer, URLDetailSerializer
from .utils import generate_short_url


class URLViewSet(viewsets.ModelViewSet):
    queryset = URL.objects.all()
    serializer_class = URLSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new shortened URL with optional expiration date.
        """
        serializer = URLSerializer(data=request.data)
        if serializer.is_valid():
            short_url = generate_short_url(serializer.validated_data["long_url"])
            instance = serializer.save(short_url=short_url)
            response_data = URLDetailSerializer(instance).data  # Use detail serializer
            return Response(response_data, status=201)
        return Response(serializer.errors, status=400)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve detailed information about a shortened URL.
        """
        instance = self.get_object()
        serializer = URLDetailSerializer(instance)
        return Response(serializer.data)

    @action(detail=False, url_path="redirect/<short_url>", methods=["get"])
    def redirect(self, request, short_url=None):
        """
        Redirect to the original URL if it exists and is not expired.
        """
        try:
            url = URL.objects.get(short_url=short_url)
            if url.is_expired():
                return HttpResponseForbidden("This link has expired.")
            return redirect(url.long_url)
        except URL.DoesNotExist:
            raise Http404("Short URL does not exist")
