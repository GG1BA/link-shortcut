from django.shortcuts import get_object_or_404
from main.models import ShortURL
from .serialize import ShortURLSerializer, ShortenURLSerializer, URLStatsSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

@api_view(['POST'])
def shorten_url_api(request):
    """
    API эндпоинт для создания короткой ссылки
    POST /api/shorten
    """
    serializer = ShortenURLSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        short_url = serializer.save()
        response_serializer = ShortURLSerializer(short_url, context={'request': request})
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class URLRedirectAPIView(APIView):
    """
    API эндпоинт для редиректа по короткому коду
    GET /api/{short_code} - редиректит на оригинальный URL
    """
    def get(self, request, short_code):
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        short_url.increment_clicks()
        return Response({
            'original_url': short_url.original_url,
            'redirect': True
        }, status=status.HTTP_302_FOUND, headers={'Location': short_url.original_url})

class URLStatsAPIView(APIView):
    """
    API эндпоинт для получения статистики по ссылке
    GET /api/stats/{short_code}
    """
    def get(self, request, short_code):
        short_url = get_object_or_404(ShortURL, short_code=short_code)
        serializer = URLStatsSerializer(short_url, context={'request': request})
        return Response(serializer.data)