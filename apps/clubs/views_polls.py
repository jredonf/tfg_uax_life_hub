"""Vistas de encuestas del modulo de clubes."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST

from .forms import ClubPollForm
from .models import ClubPoll, ClubPollOption, ClubPollVote
from .permissions import user_can_manage_club
from .view_helpers import get_published_club, redirect_to_club_section, user_is_active_member


# Ciclo de vida de encuestas.
@require_POST
@login_required
def create_poll_view(request, slug):
    """Crea una nueva encuesta para el club gestionado."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para crear encuestas.")

    form = ClubPollForm(request.POST)
    if form.is_valid():
        poll = form.save(commit=False)
        poll.club = club
        poll.created_by = request.user
        poll.save()
        for index, option_text in enumerate(form.cleaned_data["options"], start=1):
            ClubPollOption.objects.create(poll=poll, text=option_text, display_order=index)
        messages.success(request, "Encuesta creada.")
    else:
        messages.error(request, "No se pudo crear la encuesta. Revisa que tenga al menos 2 opciones validas.")
    return redirect_to_club_section(club, "encuestas")


@require_POST
@login_required
def vote_poll_view(request, slug, poll_id):
    """Registra el voto del usuario en una encuesta abierta del club."""

    club = get_published_club(slug)
    if not user_is_active_member(request.user, club) and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("Solo los miembros pueden votar en encuestas.")

    poll = get_object_or_404(ClubPoll, id=poll_id, club=club)
    if not poll.is_open:
        messages.error(request, "Esta encuesta ya esta cerrada.")
        return redirect_to_club_section(club, "encuestas")

    option = get_object_or_404(ClubPollOption, id=request.POST.get("option_id"), poll=poll)
    _, created = ClubPollVote.objects.get_or_create(
        poll=poll,
        user=request.user,
        defaults={"option": option},
    )
    if created:
        messages.success(request, "Voto registrado.")
    else:
        messages.error(request, "Ya has votado en esta encuesta.")
    return redirect_to_club_section(club, "encuestas")


@require_POST
@login_required
def close_poll_view(request, slug, poll_id):
    """Cierra manualmente una encuesta existente del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para cerrar encuestas.")

    poll = get_object_or_404(ClubPoll, id=poll_id, club=club)
    poll.status = ClubPoll.Status.CLOSED
    poll.save(update_fields=["status", "updated_at"])
    messages.success(request, "Encuesta cerrada.")
    return redirect_to_club_section(club, "encuestas")


@require_POST
@login_required
def delete_poll_view(request, slug, poll_id):
    """Elimina una encuesta del club cuando el usuario tiene permisos de gestion."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para eliminar encuestas.")

    get_object_or_404(ClubPoll, id=poll_id, club=club).delete()
    messages.success(request, "Encuesta eliminada.")
    return redirect_to_club_section(club, "encuestas")
