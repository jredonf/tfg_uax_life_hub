from django.urls import path

from .views import HomeView

app_name = "core"

# Ruta principal de la aplicacion.
urlpatterns = [
    path("", HomeView.as_view(), name="home"),
]
