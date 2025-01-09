# Django imports
from django.shortcuts import redirect
from django.http import Http404, HttpResponseForbidden

# REST Framework imports
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action

# Project file imports
from .models import URL, URLAccessLog
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
        Logs analytics data for the access.
        """
        try:
            url = URL.objects.get(short_url=short_url)
            if url.is_expired():
                return HttpResponseForbidden("This link has expired.")

            # Log access analytics
            URLAccessLog.objects.create(
                url=url,
                ip_address=self.get_client_ip(request),
                user_agent=request.META.get("HTTP_USER_AGENT", ""),
            )

            # Increment click count
            url.click_count += 1
            url.save()

            return redirect(url.long_url)
        except URL.DoesNotExist:
            raise Http404("Short URL does not exist")

    @action(detail=True, methods=["get"])
    def qr_code(self, request, pk=None):
        """
        Retrieve the QR code for the shortened URL if it exists.
        """
        try:
            url = self.get_object()
            if url.qr_code:
                qr_code_url = url.qr_code.url
                return Response({"qr_code_url": qr_code_url}, status=200)
            return Response(
                {"error": "QR code not available for this URL."}, status=404
            )
        except URL.DoesNotExist:
            raise Http404("URL does not exist")

    @action(detail=True, methods=["get"])
    def analytics(self, request, pk=None):
        """
        Retrieve analytics data for a shortened URL.
        """
        url = self.get_object()
        access_logs = url.access_logs.all().order_by("-access_time")
        analytics_data = {
            "click_count": url.click_count,
            "access_logs": [
                {
                    "access_time": log.access_time,
                    "ip_address": log.ip_address,
                    "user_agent": log.user_agent,
                }
                for log in access_logs
            ],
        }
        return Response(analytics_data, status=200)

    def get_client_ip(self, request):
        """
        Extract the client's IP address from the request.
        """
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
