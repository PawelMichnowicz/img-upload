from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Tier, User


# @admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['pk', 'email', 'tier', 'custom_tier', 'is_superuser']
    fieldsets = (
        (None, {'fields': ('email', 'tier', 'custom_tier', 'is_superuser',)}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )
    ordering = ['pk']

admin.site.register(User, UserAdmin)



@admin.register(Tier)
class TierAdmin(admin.ModelAdmin):
    ''' Define admin panel for image model '''
    list_display = ['pk', 'thumbnail_sizes', 'original_file_access', 'binary_file_access']
