from django.db import models
import random
import string

class ShortURL(models.Model):
    original_url = models.URLField(max_length=2048, verbose_name="Original link")
    short_code = models.CharField(max_length=10, unique=True, db_index=True, verbose_name="Shortcut")
    clicks = models.IntegerField(default=0, verbose_name="Redirects")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Update date")

    class Meta:
        verbose_name = "Shortcut"
        verbose_name_plural = "Shortcuts"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.short_code} -> {self.original_url}"

    def increment_clicks(self):
        self.clicks += 1
        self.save(update_fields=['clicks'])

    @staticmethod
    def generate_unique_short_code(length=6):
        characters = string.ascii_letters + string.digits
        while True:
            short_code = ''.join(random.choice(characters) for _ in range(length))
            if not ShortURL.objects.filter(short_code=short_code).exists():
                return short_code