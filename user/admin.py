from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from user.forms import CustomUserCreationForm, CustomUserChangeForm
from user.models import User


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User
    list_display = ['username', 'email', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser']


admin.site.register(User, CustomUserAdmin)

