from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Configuración del panel administrativo para usuarios de la plataforma."""

    # Amplía el panel base de Django con los datos académicos del perfil UAX.
    fieldsets = UserAdmin.fieldsets + (
        ("Perfil UAX", {"fields": ("role", "degree", "campus", "profile_image")}),
    )
    list_display = ("username", "email", "role", "is_staff")
