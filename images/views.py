import redis
from django.conf import settings
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from .models import Image
from .forms import ImageCreateForm
from actions.utils import create_action

r = redis.StrictRedis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=settings.REDIS_DB
    )

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
    total_views = r.incr(f'image:{image.id}:views')
    r.zincrby('image_ranking', 1, image.id)
    
    context= {
        'section': 'images',
        'image': image,
        'total_likes': image.users_like.count(),
        'users_like': image.users_like.all(),
        'total_views': total_views
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


@login_required
def image_ranking(request):
    template = 'image/ranking.html'
    
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in image_ranking]
    
    most_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    
    image_views = {int(id): int(r.get(f'image:{id}:views') or 0) for id in image_ranking_ids}

    for image in most_viewed:
        image.total_views = image_views.get(image.id, 0)
    
    context = {
        'section': 'image_ranking',
        'most_viewed': most_viewed
    }
    
    return render(request, template, context)