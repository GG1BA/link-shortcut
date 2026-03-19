from rest_framework import serializers
from main.models import ShortURL 

class ShortURLSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField(read_only=True)
    
    class Meta:
        model = ShortURL
        fields = ['id', 'original_url', 'short_code', 'short_url', 'clicks', 'created_at']
        read_only_fields = ['id', 'short_code', 'clicks', 'created_at']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"

class ShortenURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShortURL
        fields = ['original_url']
    
    def create(self, validated_data):
        short_code = ShortURL.generate_unique_short_code()
        short_url = ShortURL.objects.create(
            original_url=validated_data['original_url'],
            short_code=short_code
        )
        return short_url

class URLStatsSerializer(serializers.ModelSerializer):
    short_url = serializers.SerializerMethodField()
    
    class Meta:
        model = ShortURL
        fields = ['original_url', 'short_code', 'short_url', 'clicks', 'created_at']
    
    def get_short_url(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(f"/{obj.short_code}")
        return f"/{obj.short_code}"