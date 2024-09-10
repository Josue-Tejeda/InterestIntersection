import requests
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django import forms

from .models import Image
from .utils import get_file_extension

class ImageCreateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['title', 'url', 'description']
        widgets = {
            'url': forms.HiddenInput,
        }
        
    def clean_url(self):
        url = self.cleaned_data['url']
        valid_extensions = ['jpg', 'jpeg', 'png']
        extension = get_file_extension(url)
        if extension not in valid_extensions:
            raise forms.ValidationError('The given URL does not match valid image extensions.')
        return url
    
    def save(self, force_insert=False, force_update=False, commit=True):
        image = super().save(commit=False)
        image_url = self.cleaned_data['url']
        image_name = f'{slugify(image.title)}.{get_file_extension(image_url)}'
        response = requests.get(image_url)
        
        image.image.save(image_name, ContentFile(response.content), save=False)
        if commit:
            image.save()
        return image