from django import forms
from django.contrib.auth.forms import AuthenticationForm

from .models import User


# Atributos visuales reutilizados en formularios de autenticación.
AUTH_INPUT_ATTRS = {
    "class": "auth-form__input",
}

# Atributos visuales reutilizados en formularios de perfil.
PROFILE_INPUT_ATTRS = {
    "class": "profile-form__input",
}


def build_auth_attrs(autocomplete, placeholder):
    """Construye atributos comunes para los campos del acceso principal."""

    return {
        **AUTH_INPUT_ATTRS,
        "autocomplete": autocomplete,
        "placeholder": placeholder,
    }


class UAXAuthenticationForm(AuthenticationForm):
    """Formulario de autenticación adaptado al acceso del proyecto."""

    username = forms.CharField(
        label="Usuario",
        widget=forms.TextInput(
            attrs=build_auth_attrs("username", "Introduce tu usuario")
        ),
    )
    password = forms.CharField(
        label="Contraseña",
        strip=False,
        widget=forms.PasswordInput(
            attrs=build_auth_attrs("current-password", "Introduce tu contraseña")
        ),
    )
    error_messages = {
        "invalid_login": "El usuario o la contraseña no son correctos.",
        "inactive": "Esta cuenta está inactiva.",
    }


class UserProfileForm(forms.ModelForm):
    """Formulario para editar los datos visibles del perfil de usuario."""

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email", "degree", "campus", "profile_image")
        labels = {
            "first_name": "Nombre",
            "last_name": "Apellidos",
            "username": "Usuario",
            "email": "Correo electrónico",
            "degree": "Titulación",
            "campus": "Campus",
            "profile_image": "Foto de perfil",
        }
        widgets = {
            "first_name": forms.TextInput(attrs=PROFILE_INPUT_ATTRS),
            "last_name": forms.TextInput(attrs=PROFILE_INPUT_ATTRS),
            "username": forms.TextInput(attrs=PROFILE_INPUT_ATTRS),
            "email": forms.EmailInput(attrs=PROFILE_INPUT_ATTRS),
            "degree": forms.TextInput(attrs=PROFILE_INPUT_ATTRS),
            "campus": forms.TextInput(attrs=PROFILE_INPUT_ATTRS),
            "profile_image": forms.ClearableFileInput(attrs={"class": "profile-form__file"}),
        }
