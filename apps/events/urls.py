from django.urls import path

from .views import ContactPageView

app_name = "contact"

# Punto de entrada de la página pública de contacto.
urlpatterns = [
    path("", ContactPageView.as_view(), name="page"),
]
