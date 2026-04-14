from django.urls import path

from .views import SportListView

app_name = "sports"

# Punto de entrada del módulo deportivo.
urlpatterns = [
    path("", SportListView.as_view(), name="list"),
]
