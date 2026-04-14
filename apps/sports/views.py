from django.views.generic import TemplateView


class SportListView(TemplateView):
    """Muestra la página base del módulo deportivo."""

    template_name = "sports/sport_list.html"
