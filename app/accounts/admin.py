from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MCCUser
from django.utils.translation import gettext_lazy as _

@admin.register(MCCUser)
class CustomUserAdmin(UserAdmin):
    """Define admin model for custom User model with no email field."""
    readonly_fields = ("last_login", "date_joined", "date_updated")

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'date_updated')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'password1', 'password2', 'is_staff'),
        }),
    )
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    ordering = ('email',)
