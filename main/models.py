from django.db import models
from django.utils.timezone import now


class URL(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.long_url

    def is_expired(self):
        if self.expiry_date:
            return now() > self.expiry_date
        return False
