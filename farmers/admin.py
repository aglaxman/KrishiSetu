# farmers/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import FarmerAccount

@admin.register(FarmerAccount)
class FarmerAccountAdmin(UserAdmin):
    model = FarmerAccount

    list_display = (
        'email', 'username', 'first_name', 'last_name',
        'phone_number', 'verified', 'is_staff', 'is_active'
    )
    list_display_links = ('email', 'username')
    search_fields = ('email', 'username', 'first_name', 'last_name', 'phone_number')
    list_filter = ('verified', 'is_staff', 'is_active')
    ordering = ('-date_joined',)
    readonly_fields = ('last_login', 'date_joined')

    # Fields layout for the change (edit) page
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number')}),
        ('Permissions', {'fields': ('verified', 'is_staff', 'is_active', 'is_superadmin', 'is_admin')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields layout for the add (create) page in admin
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'username', 'first_name', 'last_name', 'phone_number',
                'password1', 'password2', 'is_active', 'verified'
            )
        }),
    )
