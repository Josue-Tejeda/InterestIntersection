from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    template = 'registration/dashboard.html'
    
    context = {
        'section': 'dashboard',
    }   
    return render(request, template, context)
