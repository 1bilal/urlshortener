# Django imports
from django.db import models
from django.utils.timezone import now
from django.core.files.base import ContentFile

# Third-party imports
import qrcode
from io import BytesIO


class URL(models.Model):
    long_url = models.URLField()
    short_url = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    # Analytics fields
    click_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.long_url

    def is_expired(self):
        if self.expiry_date:
            return now() > self.expiry_date
        return False

    def generate_qr_code(self):
        """Generate a QR code for the shortened URL and save it as an image."""
        qr = qrcode.make(self.long_url)  # You can use self.short_url if you prefer that
        qr_image = BytesIO()
        qr.save(qr_image, format="PNG")
        qr_image.seek(0)

        # Save QR code to a Django FileField
        self.qr_code.save(
            f"{self.short_url}.png", ContentFile(qr_image.read()), save=False
        )
        self.save()

    def save(self, *args, **kwargs):
        # Generate the QR code when a URL is created or updated
        if not self.qr_code:
            self.generate_qr_code()
        super().save(*args, **kwargs)


class URLAccessLog(models.Model):
    url = models.ForeignKey(URL, related_name="access_logs", on_delete=models.CASCADE)
    access_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"Access log for {self.url.short_url} at {self.access_time}"
