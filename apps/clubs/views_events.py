"""Vistas de eventos del módulo de clubes."""

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST

from apps.events.models import ClubEvent, ClubEventAttendance

from .forms import ClubEventForm
from .permissions import user_can_manage_club
from .view_helpers import (
    event_attendees_total,
    event_is_active,
    get_published_club,
    is_ajax_request,
    redirect_to_club_section,
    user_is_active_member,
)


# Gestión de agenda y asistencias.
@require_POST
@login_required
def create_event_view(request, slug):
    """Crea un nuevo evento asociado al club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para crear eventos.")

    form = ClubEventForm(request.POST)
    if form.is_valid():
        event = form.save(commit=False)
        event.club = club
        event.save()
        messages.success(request, "Evento creado.")
    else:
        messages.error(request, "No se pudo crear el evento.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def update_event_view(request, slug, event_id):
    """Edita la información de un evento existente del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para editar eventos.")

    event = get_object_or_404(ClubEvent, id=event_id, club=club)
    form = ClubEventForm(request.POST, instance=event)
    if form.is_valid():
        form.save()
        messages.success(request, "Evento actualizado.")
    else:
        messages.error(request, "No se pudo actualizar el evento.")
    return redirect_to_club_section(club, "eventos")


@require_POST
@login_required
def join_event_view(request, slug, event_id):
    """Inscribe al usuario en un evento controlando plazas y acompañantes."""

    club = get_published_club(slug)
    if not user_is_active_member(request.user, club) and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("Solo los miembros pueden apuntarse a eventos.")

    event = get_object_or_404(ClubEvent, id=event_id, club=club)
    if not event_is_active(event):
        if is_ajax_request(request):
            return JsonResponse(
                {"ok": False, "error": "Este evento ya ha finalizado y no admite nuevas inscripciones."},
                status=400,
            )
        messages.error(request, "Este evento ya ha finalizado y no admite nuevas inscripciones.")
        return redirect_to_club_section(club, "eventos")

    try:
        companions_count = int(request.POST.get("companions_count", 0) or 0)
    except (TypeError, ValueError):
        companions_count = -1

    if companions_count < 0 or companions_count > 10:
        error_message = "El número de acompañantes debe estar entre 0 y 10."
        if is_ajax_request(request):
            return JsonResponse({"ok": False, "error": error_message}, status=400)
        messages.error(request, error_message)
        return redirect_to_club_section(club, "eventos")

    # Se bloquea el evento para evitar sobreventa de plazas en concurrencia.
    with transaction.atomic():
        event = ClubEvent.objects.select_for_update().get(id=event.id, club=club)
        if not event_is_active(event):
            if is_ajax_request(request):
                return JsonResponse(
                    {"ok": False, "error": "Este evento ya ha finalizado y no admite nuevas inscripciones."},
                    status=400,
                )
            messages.error(request, "Este evento ya ha finalizado y no admite nuevas inscripciones.")
            return redirect_to_club_section(club, "eventos")

        existing_attendance = ClubEventAttendance.objects.filter(event=event, user=request.user).first()
        if existing_attendance:
            if is_ajax_request(request):
                return JsonResponse(
                    {
                        "ok": True,
                        "already_joined": True,
                        "attendees_total": event_attendees_total(event),
                        "attendance_id": existing_attendance.id,
                        "companions_count": existing_attendance.companions_count,
                    }
                )
            messages.info(request, "Ya estabas apuntado a este evento.")
            return redirect_to_club_section(club, "eventos")

        attendees_total = event_attendees_total(event)
        required_slots = 1 + companions_count
        if event.capacity and attendees_total + required_slots > event.capacity:
            if is_ajax_request(request):
                return JsonResponse(
                    {"ok": False, "error": "No quedan plazas disponibles para este evento."},
                    status=400,
                )
            messages.error(request, "No quedan plazas disponibles para este evento.")
            return redirect_to_club_section(club, "eventos")

        attendance = ClubEventAttendance.objects.create(
            event=event,
            user=request.user,
            companions_count=companions_count,
        )
        attendees_total += required_slots

    if is_ajax_request(request):
        return JsonResponse(
            {
                "ok": True,
                "attendees_total": attendees_total,
                "attendance_id": attendance.id,
                "user_display_name": request.user.display_name,
                "companions_count": companions_count,
                "delete_url": reverse(
                    "clubs:delete_event_attendance",
                    kwargs={"slug": club.slug, "event_id": event.id, "attendance_id": attendance.id},
                ),
                "update_url": reverse(
                    "clubs:update_event_attendance",
                    kwargs={"slug": club.slug, "event_id": event.id, "attendance_id": attendance.id},
                ),
            }
        )
    messages.success(request, "Te has apuntado al evento.")
    return redirect_to_club_section(club, "eventos")


@require_POST
@login_required
def update_event_attendance_view(request, slug, event_id, attendance_id):
    """Actualiza el número de acompañantes de una asistencia existente."""

    club = get_published_club(slug)
    event = get_object_or_404(ClubEvent, id=event_id, club=club)
    attendance = get_object_or_404(ClubEventAttendance, id=attendance_id, event=event)

    if attendance.user_id != request.user.id and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para modificar esta asistencia.")

    if not event_is_active(event) and not user_can_manage_club(request.user, club):
        if is_ajax_request(request):
            return JsonResponse(
                {"ok": False, "error": "Este evento ya ha finalizado y no se pueden modificar asistentes."},
                status=400,
            )
        messages.error(request, "Este evento ya ha finalizado y no se pueden modificar asistentes.")
        return redirect_to_club_section(club, "eventos")

    try:
        companions_count = int(request.POST.get("companions_count", 0) or 0)
    except (TypeError, ValueError):
        companions_count = -1

    if companions_count < 0 or companions_count > 10:
        error_message = "El número de acompañantes debe estar entre 0 y 10."
        if is_ajax_request(request):
            return JsonResponse({"ok": False, "error": error_message}, status=400)
        messages.error(request, error_message)
        return redirect_to_club_section(club, "eventos")

    # Recalcula disponibilidad de forma atómica para evitar inconsistencias.
    with transaction.atomic():
        attendance = ClubEventAttendance.objects.select_for_update().select_related("event", "user").get(
            id=attendance.id,
            event=event,
        )
        attendees_total_without_current = event_attendees_total(event) - (1 + attendance.companions_count)
        required_slots = 1 + companions_count

        if event.capacity and attendees_total_without_current + required_slots > event.capacity:
            if is_ajax_request(request):
                return JsonResponse(
                    {"ok": False, "error": "No quedan plazas disponibles para este evento."},
                    status=400,
                )
            messages.error(request, "No quedan plazas disponibles para este evento.")
            return redirect_to_club_section(club, "eventos")

        attendance.companions_count = companions_count
        attendance.save(update_fields=["companions_count"])
        attendees_total = attendees_total_without_current + required_slots

    if is_ajax_request(request):
        return JsonResponse(
            {
                "ok": True,
                "attendees_total": attendees_total,
                "attendance_id": attendance.id,
                "user_display_name": attendance.user.display_name,
                "companions_count": companions_count,
                "delete_url": reverse(
                    "clubs:delete_event_attendance",
                    kwargs={"slug": club.slug, "event_id": event.id, "attendance_id": attendance.id},
                ),
                "update_url": reverse(
                    "clubs:update_event_attendance",
                    kwargs={"slug": club.slug, "event_id": event.id, "attendance_id": attendance.id},
                ),
            }
        )

    messages.success(request, "Acompanantes actualizados.")
    return redirect_to_club_section(club, "eventos")


@require_POST
@login_required
def delete_event_attendance_view(request, slug, event_id, attendance_id):
    """Cancela una asistencia a evento si el usuario puede gestionarla."""

    club = get_published_club(slug)
    event = get_object_or_404(ClubEvent, id=event_id, club=club)
    attendance = get_object_or_404(ClubEventAttendance, id=attendance_id, event=event)

    if attendance.user_id != request.user.id and not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para eliminar esta asistencia.")

    if not event_is_active(event) and not user_can_manage_club(request.user, club):
        if is_ajax_request(request):
            return JsonResponse(
                {"ok": False, "error": "Este evento ya ha finalizado y no se pueden modificar asistentes."},
                status=400,
            )
        messages.error(request, "Este evento ya ha finalizado y no se pueden modificar asistentes.")
        return redirect_to_club_section(club, "eventos")

    attendance.delete()
    if is_ajax_request(request):
        return JsonResponse({"ok": True, "attendees_total": event_attendees_total(event)})

    messages.success(request, "Asistencia eliminada.")
    return redirect_to_club_section(club, "eventos")


@require_POST
@login_required
def delete_event_view(request, slug, event_id):
    """Elimina un evento del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para eliminar eventos.")

    get_object_or_404(ClubEvent, id=event_id, club=club).delete()
    messages.success(request, "Evento eliminado.")
    return redirect("clubs:detail", slug=club.slug)
