from django.utils.timezone import now
from rest_framework import serializers
from urllib.parse import urlparse
from .models import URL
from .utils import generate_short_url


class URLSerializer(serializers.ModelSerializer):
    short_url = serializers.CharField(
        required=False,  # Allow the short_url to be optional for the creation
        allow_blank=True,
    )

    class Meta:
        model = URL
        fields = ["long_url", "expiry_date", "short_url"]

    def validate_expiry_date(self, value):
        """Ensure expiry date is not in the past."""
        if value and value < now():
            raise serializers.ValidationError("Expiry date cannot be in the past.")
        return value

    def validate_long_url(self, value):
        """Validate that the long_url is a well-formed URL."""
        parsed_url = urlparse(value)
        if not parsed_url.scheme or not parsed_url.netloc:
            raise serializers.ValidationError("Invalid URL format.")
        return value

    def validate_short_url(self, value):
        """Validate that the custom short_url is unique."""
        if value and URL.objects.filter(short_url=value).exists():
            raise serializers.ValidationError("Short URL already exists.")
        return value

    def create(self, validated_data):
        """Generate a short URL or use custom short_url, and create the URL instance."""
        short_url = validated_data.get("short_url", None)
        if not short_url:
            short_url = generate_short_url(
                validated_data["long_url"]
            )  # Generate if not provided

        # Ensure the custom short URL is unique
        validated_data["short_url"] = short_url

        url_instance = URL.objects.create(**validated_data)
        return url_instance


class URLDetailSerializer(serializers.ModelSerializer):
    qr_code_url = serializers.SerializerMethodField()

    class Meta:
        model = URL
        fields = [
            "long_url",
            "short_url",
            "created_at",
            "updated_at",
            "expiry_date",
            "qr_code_url",
            "click_count",  # Add click count for analytics
        ]

    def get_qr_code_url(self, obj):
        """Get the full URL of the QR code image."""
        if obj.qr_code:
            return obj.qr_code.url  # Returns the relative URL to the QR code
        return None


class URLAnalyticsSerializer(serializers.ModelSerializer):
    access_logs = serializers.SerializerMethodField()

    class Meta:
        model = URL
        fields = ["short_url", "click_count", "access_logs"]

    def get_access_logs(self, obj):
        """Retrieve access logs for the URL."""
        return [
            {
                "access_time": log.access_time,
                "ip_address": log.ip_address,
                "user_agent": log.user_agent,
            }
            for log in obj.access_logs.all().order_by("-access_time")
        ]
