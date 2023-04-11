from django.contrib import admin
from django.db import models
from .models import Users
from .forms_auth import UsersCreationFrom
from django.contrib.auth.admin import UserAdmin


# Register your models here.

class UsersAdmin(UserAdmin):
    model = Users
    add_form = UsersCreationFrom
    list_display = ('email', 'first_name', 'last_name', 'date_joined', 'is_staff')
    ordering = ('date_joined',)
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login',)
    list_filter = ('is_staff',)

    fieldsets = (
        (
            'User profile',
            {
                'fields':
                (
                    'first_name',
                    'last_name',
                    'password',
                    'date_joined',
                    'last_login',
                    'birthday',
                    'address',
                    'phone',
                    'facebook',
                )
            }
        ),
        (
            'User role',
            {
                'fields': (
                    'is_superuser',
                    'is_active',
                    'is_staff',
                )
            }
        )
    )
    add_fieldsets = (
        None,
        {
            'fields': (
                'email',
                'password1',
                'password2',
            )
        }
    ),


admin.site.register(Users, UsersAdmin)