from django import forms
from .models import ShortURL

class ShortURLForm(forms.ModelForm):
    original_url = forms.CharField()

    class Meta:
        model = ShortURL
        fields = ['original_url']

    def clean_original_url(self):
        url = self.cleaned_data.get('original_url')

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        return url

