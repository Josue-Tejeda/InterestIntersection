from django.contrib import admin
from .models import Profile, Contact

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'birth_date', 'avatar']
    

@admin.register(Contact)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user_from', 'user_to', 'created_at']
