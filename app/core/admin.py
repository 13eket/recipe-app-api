"""
Django admin customization.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.models import User


class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ['id']
    list_display = ['email', 'name']
    fieldsets = (
        (None, {
            'fields': ('email', 'password')
        }),
        ('Personal Info', {
            'fields': ('name',)
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_superuser', 'is_staff')
        }),
        ('Important dates', {
            'fields': ('last_login',)
        }),
    )
    readonly_fields = ['last_login']


admin.site.register(User, UserAdmin)
