from django.contrib.auth import views as auth_views
from django.urls import path

from .forms import UAXAuthenticationForm
from .views import ProfileView, modal_login

app_name = "accounts"

# Rutas relacionadas con autenticación y gestión del perfil personal.
urlpatterns = [
    path("profile/", ProfileView.as_view(), name="profile"),
    path("login/modal/", modal_login, name="modal_login"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="registration/login.html",
            authentication_form=UAXAuthenticationForm,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]
