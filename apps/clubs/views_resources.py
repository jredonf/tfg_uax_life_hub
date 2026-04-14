"""Vistas de recursos compartidos del modulo de clubes."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST

from .forms import ClubResourceForm
from .models import ClubResource
from .permissions import user_can_manage_club
from .view_helpers import get_published_club, user_is_active_member


# Recursos compartidos del club.
@require_POST
@login_required
def upload_resource_view(request, slug):
    """Sube un recurso compartido asociado al club."""

    club = get_published_club(slug)
    if not user_is_active_member(request.user, club) and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("Solo los miembros pueden subir recursos.")

    form = ClubResourceForm(request.POST, request.FILES)
    if form.is_valid():
        resource = form.save(commit=False)
        resource.club = club
        resource.uploaded_by = request.user
        resource.save()
        messages.success(request, "Recurso subido.")
    else:
        messages.error(request, "No se pudo subir el recurso.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def delete_resource_view(request, slug, resource_id):
    """Elimina un recurso si el actor es su autor o gestiona el club."""

    club = get_published_club(slug)
    resource = get_object_or_404(ClubResource, id=resource_id, club=club)

    if resource.uploaded_by_id != request.user.id and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para eliminar este recurso.")

    resource.delete()
    messages.success(request, "Recurso eliminado.")
    return redirect("clubs:detail", slug=club.slug)
