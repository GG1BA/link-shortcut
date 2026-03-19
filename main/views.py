from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .models import ShortURL
from .forms import ShortURLForm

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
