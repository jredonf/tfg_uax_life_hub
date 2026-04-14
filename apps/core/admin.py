from django.contrib import admin

from .models import HomePageSettings


@admin.register(HomePageSettings)
class HomePageSettingsAdmin(admin.ModelAdmin):
    """Panel para mantener la configuración editable de la portada."""

    fields = (
        "hero_title",
        "hero_description",
        "hero_button_text_logged_out",
        "hero_button_text_logged_in",
        "hero_image",
    )

    def has_add_permission(self, request):
        # Se fuerza un único registro para tratar la configuración como singleton.
        if HomePageSettings.objects.exists():
            return False
        return super().has_add_permission(request)
