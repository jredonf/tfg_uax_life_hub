from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import UpdateView

from .forms import UAXAuthenticationForm, UserProfileForm


def collect_form_errors(form):
    """Agrupa los errores del formulario en una lista simple para AJAX."""

    errors = []
    for field_errors in form.errors.values():
        errors.extend(field_errors)
    return errors


@require_POST
def modal_login(request):
    """Gestiona el inicio de sesión desde el modal sin recargar la página."""

    form = UAXAuthenticationForm(request=request, data=request.POST)

    if form.is_valid():
        auth_login(request, form.get_user())
        return JsonResponse(
            {
                "ok": True,
                "header_html": render_to_string("includes/header.html", request=request),
            }
        )

    return JsonResponse({"ok": False, "errors": collect_form_errors(form)}, status=400)


class ProfileView(LoginRequiredMixin, UpdateView):
    """Permite al usuario autenticado actualizar su propio perfil."""

    form_class = UserProfileForm
    template_name = "accounts/profile.html"
    success_url = reverse_lazy("accounts:profile")

    def get_object(self, queryset=None):
        # La vista siempre edita el usuario autenticado.
        return self.request.user

    def form_valid(self, form):
        # Informa al usuario cuando los cambios se guardan correctamente.
        messages.success(self.request, "Tu perfil se ha actualizado correctamente.")
        return super().form_valid(form)
