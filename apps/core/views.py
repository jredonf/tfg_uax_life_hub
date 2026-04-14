from django.views.generic import TemplateView

from .models import HomePageSettings


class HomeView(TemplateView):
    """Renderiza la portada principal con la configuración editable actual."""

    template_name = "core/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # La home utiliza el primer registro disponible como configuración activa.
        context["home_settings"] = HomePageSettings.objects.first()
        return context
