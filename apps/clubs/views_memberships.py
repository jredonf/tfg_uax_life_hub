"""Vistas de miembros y permisos del modulo de clubes."""

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.events.models import ClubEventAttendance

from .models import ClubMembership
from .permissions import user_can_manage_club
from .view_helpers import (
    get_published_club,
    redirect_to_club_section,
    user_can_remove_member,
    user_can_update_member_role,
)


# Operaciones de jerarquia interna.
@require_POST
@login_required
def update_member_role_view(request, slug, membership_id):
    """Modifica el rol de una membresia si la jerarquia del actor lo permite."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para modificar roles en este club.")

    membership = get_object_or_404(
        ClubMembership,
        id=membership_id,
        club=club,
        status=ClubMembership.Status.APPROVED,
        left_at__isnull=True,
    )
    role_in_club = request.POST.get("role_in_club")
    if role_in_club not in ClubMembership.RoleInClub.values:
        messages.error(request, "El rol seleccionado no es valido.")
        return redirect("clubs:detail", slug=club.slug)

    if not user_can_update_member_role(request.user, club, membership, role_in_club):
        messages.error(request, "No puedes modificar roles de usuarios con un rango igual o superior al tuyo.")
        return redirect("clubs:detail", slug=club.slug)

    membership.role_in_club = role_in_club
    membership.save(update_fields=["role_in_club"])
    messages.success(request, f"Rol actualizado para {membership.user.display_name}.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def remove_member_view(request, slug, membership_id):
    """Expulsa a un miembro del club y libera sus plazas de eventos activos."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para eliminar miembros de este club.")

    membership = get_object_or_404(
        ClubMembership,
        id=membership_id,
        club=club,
        status=ClubMembership.Status.APPROVED,
        left_at__isnull=True,
    )
    if not user_can_remove_member(request.user, club, membership):
        messages.error(request, "No puedes eliminar a un miembro con rango igual o superior al tuyo.")
        return redirect_to_club_section(club, "miembros")

    removal_reason = request.POST.get("removal_reason", "")
    removal_reason_other = request.POST.get("removal_reason_other", "").strip()

    if removal_reason not in ClubMembership.RemovalReason.values:
        messages.error(request, "Selecciona una causa para eliminar al miembro.")
        return redirect_to_club_section(club, "miembros")

    if removal_reason == ClubMembership.RemovalReason.OTHER and not removal_reason_other:
        messages.error(request, "Indica el motivo cuando selecciones Otros.")
        return redirect_to_club_section(club, "miembros")

    if len(removal_reason_other) > 100:
        messages.error(request, "El motivo no puede superar los 100 caracteres.")
        return redirect_to_club_section(club, "miembros")

    removal_cutoff = timezone.now() - timedelta(hours=2)
    # Ambas operaciones deben ejecutarse como una unica transaccion coherente.
    with transaction.atomic():
        removed_attendances_total, _ = ClubEventAttendance.objects.filter(
            user=membership.user,
            event__club=club,
            event__start_datetime__gte=removal_cutoff,
        ).delete()
        membership.status = ClubMembership.Status.CANCELLED
        membership.left_at = timezone.now()
        membership.removal_reason = removal_reason
        membership.removal_reason_other = removal_reason_other if removal_reason == ClubMembership.RemovalReason.OTHER else ""
        membership.save(update_fields=["status", "left_at", "removal_reason", "removal_reason_other"])

    if removed_attendances_total:
        messages.success(
            request,
            f"{membership.user.display_name} se ha eliminado del club y se han liberado {removed_attendances_total} plaza(s) en eventos activos.",
        )
    else:
        messages.success(request, f"{membership.user.display_name} se ha eliminado del club.")
    return redirect_to_club_section(club, "miembros")
