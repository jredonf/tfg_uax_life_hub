"""Utilidades compartidas para las vistas del módulo de clubes."""

from datetime import timedelta

from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone

from apps.events.models import ClubEventAttendance

from .models import Club, ClubMembership


# Jerarquía interna usada para validar cambios de rol y expulsiones.
CLUB_ROLE_RANKS = {
    ClubMembership.RoleInClub.MEMBER: 10,
    ClubMembership.RoleInClub.CAPTAIN: 20,
    ClubMembership.RoleInClub.MANAGER: 30,
    ClubMembership.RoleInClub.ADMIN: 40,
}


def user_is_active_member(user, club):
    """Comprueba si el usuario mantiene una membresía activa en el club."""

    if not user.is_authenticated:
        return False
    return club.memberships.filter(
        user=user,
        status=ClubMembership.Status.APPROVED,
        left_at__isnull=True,
    ).exists()


def get_published_club(slug):
    """Recupera un club publicado o devuelve error 404 si no existe."""

    return get_object_or_404(Club, slug=slug, current_status=Club.Status.PUBLISHED)


def is_ajax_request(request):
    """Detecta peticiones AJAX basadas en la cabecera habitual."""

    return request.headers.get("x-requested-with") == "XMLHttpRequest"


def redirect_to_club_section(club, section):
    """Redirige al detalle del club anclando una sección concreta."""

    return redirect(f"{reverse('clubs:detail', kwargs={'slug': club.slug})}#{section}")


def event_attendees_total(event):
    """Calcula el total de plazas ocupadas contando acompañantes."""

    return sum(
        1 + attendance.companions_count
        for attendance in ClubEventAttendance.objects.filter(event=event)
    )


def event_is_active(event):
    """Considera activo un evento hasta dos horas después de su inicio."""

    return timezone.now() <= event.start_datetime + timedelta(hours=2)


def user_is_global_admin(user):
    """Determina si el usuario puede operar con privilegios globales."""

    return user.is_authenticated and (user.is_superuser or getattr(user, "role", "") == "admin")


def get_user_club_role_rank(user, club):
    """Obtiene el rango operativo del usuario dentro del club."""

    if not user.is_authenticated:
        return 0

    if user_is_global_admin(user):
        return 100

    membership = club.memberships.filter(
        user=user,
        status=ClubMembership.Status.APPROVED,
        left_at__isnull=True,
    ).first()
    if not membership:
        return 0
    return CLUB_ROLE_RANKS.get(membership.role_in_club, 0)


def user_can_update_member_role(user, club, target_membership, new_role):
    """Valida si el actor puede cambiar el rol de una membresía concreta."""

    actor_rank = get_user_club_role_rank(user, club)
    target_rank = CLUB_ROLE_RANKS.get(target_membership.role_in_club, 0)
    new_role_rank = CLUB_ROLE_RANKS.get(new_role, 0)

    if target_membership.user_id == user.id:
        if user_is_global_admin(user):
            return True
        return actor_rank > new_role_rank

    if user_is_global_admin(user):
        return True

    return actor_rank > target_rank and actor_rank > new_role_rank


def user_can_remove_member(user, club, target_membership):
    """Comprueba si el actor puede expulsar a otro miembro del club."""

    if target_membership.user_id == user.id:
        return False

    if user_is_global_admin(user):
        return True

    actor_rank = get_user_club_role_rank(user, club)
    target_rank = CLUB_ROLE_RANKS.get(target_membership.role_in_club, 0)
    return actor_rank > target_rank
