from django.contrib import admin
from .models import ShortURL

@admin.register(ShortURL)
class ShortURLAdmin(admin.ModelAdmin):
    list_display = ('short_code', 'original_url', 'clicks', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('original_url', 'short_code')
    readonly_fields = ('short_code', 'clicks', 'created_at', 'updated_at')
    fieldsets = (
        ('Info', {
            'fields': ('original_url', 'short_code')
        }),
        ('Stats', {
            'fields': ('clicks', 'created_at', 'updated_at')
        }),
    )