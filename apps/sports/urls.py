from django.urls import path

from .views import SportListView, update_match_result_view

app_name = "sports"

# Punto de entrada del modulo deportivo.
urlpatterns = [
    path("", SportListView.as_view(), name="list"),
    path("partidos/<int:match_id>/resultado/", update_match_result_view, name="update_match_result"),
]
