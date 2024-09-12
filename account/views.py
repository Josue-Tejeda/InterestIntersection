from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .forms import UserRegistrationForm, UserEditForm, ProfileEditForm
from .models import Contact, Profile
from actions.models import Action
from actions.utils import create_action

User = get_user_model()

@login_required
def dashboard(request):
    template = 'registration/dashboard.html'
    actions = Action.objects.exclude(user=request.user)
    following_ids = request.user.following.values_list('id', flat=True)
    
    if following_ids:
        actions = actions.filter(user_id__in=following_ids)
        actions = actions.select_related('user', 'user__profile').prefetch_related('target')[:10]
    
    context = {
        'section': 'dashboard',
        'actions': actions,
    }   
    return render(request, template, context)


def register(request):
    if request.method == 'POST':
        user_form  = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            Profile.objects.create(user=new_user)
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        
        return render(request, 'account/register.html', {'user_form': user_form})
    

@login_required
def edit(request):
    template = 'account/edit.html'
    
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(
                request,
                'Profile updated successfully'
            )
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    
    return render(request, template, context)


@login_required
def user_list(request):
    template = 'user/list.html'
    users = User.objects.filter(is_active=True)
    paginator = Paginator(users, 8)
    page = request.GET.get('page')
    
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    
    context = {
        'section': 'people',
        'users': users,
    }
    
    return render(request, template, context)


@login_required
def user_detail(request, username):
    template = 'user/detail.html'
    user_detail = get_object_or_404(User, username=username, is_active=True)
    
    context = {
        'section': 'people',
        'user_detail': user_detail,
    }
    
    return render(request, template, context)


@login_required
@require_POST
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    
    if user_id and action:
        try:
            user = User.objects.get(id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
                create_action(request.user, 'is following', user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})