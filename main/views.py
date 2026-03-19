from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import ShortURL
from .forms import ShortURLForm
from .serialize import ShortURLSerializer, ShortenURLSerializer, URLStatsSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

def index(request):
    short_url = None
    if request.method == 'POST':
        form = ShortURLForm(request.POST)
        if form.is_valid():
            short_url_obj = form.save(commit=False)
            short_url_obj.short_code = ShortURL.generate_unique_short_code()
            short_url_obj.save()
            
            short_url = request.build_absolute_uri(reverse('redirect', args=[short_url_obj.short_code]))
            
            messages.success(request, 'Shortcut generated!')
    else:
        form = ShortURLForm()
    
    recent_links = ShortURL.objects.all()[:5]
    
    return render(request, 'index.html', {
        'form': form,
        'short_url': short_url,
        'recent_links': recent_links
    })

def redirect_to_original(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    short_url.increment_clicks()
    return HttpResponseRedirect(short_url.original_url)

def link_stats(request, short_code):
    short_url = get_object_or_404(ShortURL, short_code=short_code)
    return render(request, 'stats.html', {'short_url': short_url})

def all_links(request):
    links = ShortURL.objects.all()
    return render(request, 'all_links.html', {'links': links})





# REST API

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
        # Увеличиваем счетчик кликов
        short_url.increment_clicks()
        # Возвращаем оригинальный URL для редиректа
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