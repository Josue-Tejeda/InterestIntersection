from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Image
from .forms import ImageCreateForm

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added successfully')
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCreateForm(data=request.GET)
        return render(request, 'image/create.html', {'section': 'images', 'form': form})
    
    
def image_detail(request, id, slug):
    template = 'image/detail.html'
    image = get_object_or_404(Image, id=id, slug=slug)
    context= {
        'section': 'images',
        'image': image
        }
    
    return render(request, template, context)