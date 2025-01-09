from django.utils.timezone import now
from rest_framework import serializers
from .models import URL


class URLSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ["long_url", "expiry_date"]

    def validate_expiry_date(self, value):
        if value and value < now():
            raise serializers.ValidationError("Expiry date cannot be in the past.")
        return value


class URLDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = URL
        fields = ["long_url", "short_url", "created_at", "updated_at", "expiry_date"]
