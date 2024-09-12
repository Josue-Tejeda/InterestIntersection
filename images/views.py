from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Image
from .forms import ImageCreateForm
from actions.utils import create_action

@login_required
def image_create(request):
    if request.method == 'POST':
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            new_image.user = request.user
            new_image.save()
            create_action(request.user, 'bookmarked image', new_image)
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
        'image': image,
        'total_likes': image.users_like.count(),
        'users_like': image.users_like.all()
        }
    
    return render(request, template, context)


@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
                create_action(request.user, 'likes', image)
            else:
                image.users_like.remove(request.user)
            
            return JsonResponse({'status': 'ok'})
        except Image.DoesNotExist:
            pass
        
    return JsonResponse({'status': 'error'})


@login_required
def image_list(request):
    images = Image.objects.all().order_by('-created_at')
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    images_only = request.GET.get('images_only')
    
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if images_only:
            return HttpResponse('')
        images = paginator.page(paginator.num_pages)

    template = 'image/list_images.html' if images_only else 'image/list.html'
    return render(request, template, {'section': 'images', 'images': images})