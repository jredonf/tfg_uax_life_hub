"""Vistas públicas y generales del módulo de clubes."""

from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, Count, IntegerField, Prefetch, Q, Value, When
from django.http import HttpResponseForbidden, JsonResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, TemplateView

from apps.accounts.forms import UAXAuthenticationForm
from apps.events.models import ClubEvent, ClubEventAttendance

from .forms import (
    ClubContactForm,
    ClubEventForm,
    ClubGeneralForm,
    ClubPollForm,
    ClubPostCommentForm,
    ClubPostForm,
    ClubResourceForm,
)
from .models import Club, ClubCategory, ClubMembership, ClubPoll, ClubPollVote, ClubPostLike
from .permissions import user_can_manage_club
from .services import request_membership
from .view_helpers import (
    CLUB_ROLE_RANKS,
    get_published_club,
    get_user_club_role_rank,
    user_can_remove_member,
    user_is_active_member,
    user_is_global_admin,
)


# Vistas de navegación pública.
class ClubListView(TemplateView):
    """Muestra el catálogo de clubes agrupado por categorías publicadas."""

    template_name = "clubs/club_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        joined_club_ids = []
        if self.request.user.is_authenticated:
            # Prioriza los clubes del usuario para mejorar su descubrimiento.
            joined_club_ids = list(
                self.request.user.club_memberships.filter(
                    status=ClubMembership.Status.APPROVED,
                    left_at__isnull=True,
                ).values_list("club_id", flat=True)
            )
        published_clubs = Club.objects.filter(current_status=Club.Status.PUBLISHED).annotate(
            active_members_total=Count(
                "memberships",
                filter=Q(
                    memberships__status=ClubMembership.Status.APPROVED,
                    memberships__left_at__isnull=True,
                ),
                distinct=True,
            ),
            membership_priority=Case(
                When(id__in=joined_club_ids, then=Value(0)),
                default=Value(1),
                output_field=IntegerField(),
            ),
        ).order_by("membership_priority", "-active_members_total", "name")
        # Solo se muestran categorías que contienen al menos un club publicado.
        context["categories"] = (
            ClubCategory.objects.annotate(
                published_clubs_count=Count(
                    "clubs",
                    filter=Q(clubs__current_status=Club.Status.PUBLISHED),
                )
            )
            .filter(published_clubs_count__gt=0)
            .prefetch_related(Prefetch("clubs", queryset=published_clubs, to_attr="published_clubs"))
            .order_by("display_order", "name")
        )
        context["joined_club_ids"] = joined_club_ids
        context["login_form"] = UAXAuthenticationForm()
        return context


class ClubDetailView(DetailView):
    """Construye la vista completa de detalle y gestion de un club publicado."""

    template_name = "clubs/club_detail.html"
    model = Club
    context_object_name = "club"
    slug_field = "slug"
    slug_url_kwarg = "slug"

    def get_queryset(self):
        # Anota el total de miembros activos para evitar recálculos repetidos.
        return (
            Club.objects.filter(current_status=Club.Status.PUBLISHED)
            .select_related("category")
            .annotate(
                active_members_total=Count(
                    "memberships",
                    filter=Q(
                        memberships__status=ClubMembership.Status.APPROVED,
                        memberships__left_at__isnull=True,
                    ),
                    distinct=True,
                )
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        club = self.object
        is_member = user_is_active_member(self.request.user, club)
        actual_can_manage = user_can_manage_club(self.request.user, club)
        actor_rank = get_user_club_role_rank(self.request.user, club)
        is_global_admin = user_is_global_admin(self.request.user)
        # Los gestores pueden alternar entre vista de gestion y vista de miembro.
        can_toggle_member_view = is_member and (
            is_global_admin or actor_rank >= CLUB_ROLE_RANKS[ClubMembership.RoleInClub.CAPTAIN]
        )
        view_as_member = can_toggle_member_view and self.request.GET.get("view") == "member"
        can_manage = actual_can_manage and not view_as_member
        members = list(
            club.memberships.filter(status=ClubMembership.Status.APPROVED, left_at__isnull=True)
            .select_related("user")
            .order_by("joined_at", "user__first_name", "user__username")
        )
        for membership in members:
            # Calcula una antiguedad legible para mostrar en la interfaz.
            elapsed = timezone.now() - membership.joined_at
            if elapsed.days >= 1:
                membership.tenure_label = f"{elapsed.days} día{'s' if elapsed.days != 1 else ''}"
            else:
                hours = elapsed.seconds // 3600
                membership.tenure_label = f"{hours} hora{'s' if hours != 1 else ''}" if hours >= 1 else "Nuevo"
            is_own_membership = membership.user_id == self.request.user.id
            can_update_other = can_manage and actor_rank > CLUB_ROLE_RANKS.get(membership.role_in_club, 0)
            can_update_self = is_own_membership and actor_rank > CLUB_ROLE_RANKS[ClubMembership.RoleInClub.MEMBER]
            # Expone permisos derivados para simplificar la plantilla.
            membership.can_update_role = not view_as_member and (is_global_admin or can_update_other or can_update_self)
            membership.editable_role_choices = [
                (role_value, role_label)
                for role_value, role_label in ClubMembership.RoleInClub.choices
                if role_value == membership.role_in_club
                or is_global_admin
                or actor_rank > CLUB_ROLE_RANKS.get(role_value, 0)
            ]
            membership.can_remove_member = not view_as_member and can_manage and user_can_remove_member(
                self.request.user,
                club,
                membership,
            )
        posts = (
            club.posts.select_related("author")
            .prefetch_related("comments__author", "likes")
            .annotate(likes_total=Count("likes", distinct=True), comments_total=Count("comments", distinct=True))
            .order_by("-created_at")
        )
        events = list(
            ClubEvent.objects.filter(club=club)
            .prefetch_related("attendances__user")
            .order_by("-start_datetime")
        )
        now = timezone.now()
        for event in events:
            # Enriquece cada evento con estado, asistentes y datos del usuario actual.
            event.attendees_total = sum(1 + attendance.companions_count for attendance in event.attendances.all())
            event.is_active_status = now <= event.start_datetime + timedelta(hours=2)
            event.status_label = "Activo" if event.is_active_status else "Finalizado"
            event.current_user_attendance = None
            event.display_attendances = list(event.attendances.all())
            if self.request.user.is_authenticated:
                event.current_user_attendance = next(
                    (
                        attendance
                        for attendance in event.attendances.all()
                        if attendance.user_id == self.request.user.id
                    ),
                    None,
                )
                event.display_attendances.sort(
                    key=lambda attendance: (
                        0 if attendance.user_id == self.request.user.id else 1,
                        attendance.joined_at,
                    )
                )
        # Prioriza eventos activos y acerca los proximos al inicio de la lista.
        events.sort(
            key=lambda event: (
                0 if event.is_active_status else 1,
                abs((event.start_datetime - now).total_seconds()) if event.is_active_status else 0,
                -event.start_datetime.timestamp() if not event.is_active_status else event.start_datetime.timestamp(),
            )
        )
        active_events_total = sum(1 for event in events if event.is_active_status)
        liked_post_ids = []
        event_attendance_ids = []
        poll_vote_option_ids = []
        if self.request.user.is_authenticated:
            liked_post_ids = list(
                ClubPostLike.objects.filter(post__club=club, user=self.request.user).values_list(
                    "post_id",
                    flat=True,
                )
            )
            event_attendance_ids = list(
                ClubEventAttendance.objects.filter(event__club=club, user=self.request.user).values_list(
                    "event_id",
                    flat=True,
                )
            )
            poll_vote_option_ids = list(
                ClubPollVote.objects.filter(poll__club=club, user=self.request.user).values_list(
                    "option_id",
                    flat=True,
                )
            )

        visible_polls = club.polls.select_related("created_by").prefetch_related("options__votes", "votes")
        # Los visitantes solo pueden consultar encuestas públicas.
        if not is_member and not actual_can_manage:
            visible_polls = visible_polls.filter(visibility=ClubPoll.Visibility.PUBLIC)
        polls = list(visible_polls.order_by("-created_at"))
        for poll in polls:
            # Calcula indicadores de votacion directamente consumibles por la plantilla.
            poll.is_open_status = poll.is_open
            poll.user_has_voted = self.request.user.is_authenticated and poll.votes.filter(user=self.request.user).exists()
            poll.can_vote = (
                poll.is_open_status
                and self.request.user.is_authenticated
                and (is_member or actual_can_manage)
                and not poll.user_has_voted
            )
            poll.votes_total = poll.votes.count()
            for option in poll.options.all():
                option.votes_total = option.votes.count()
                option.percentage = round((option.votes_total / poll.votes_total) * 100) if poll.votes_total else 0
                option.is_selected_by_user = option.id in poll_vote_option_ids

        context.update(
            {
                "is_member": is_member,
                "can_manage": can_manage,
                "can_toggle_member_view": can_toggle_member_view,
                "view_as_member": view_as_member,
                "members": members,
                "members_total": len(members),
                "membership_role_choices": ClubMembership.RoleInClub.choices,
                "membership_removal_reason_choices": ClubMembership.RemovalReason.choices,
                "posts": posts,
                "events": events,
                "events_total": len(events),
                "active_events_total": active_events_total,
                "liked_post_ids": liked_post_ids,
                "event_attendance_ids": event_attendance_ids,
                "polls": polls,
                "poll_form": ClubPollForm(),
                "resources": club.resources.select_related("uploaded_by").all(),
                "general_form": ClubGeneralForm(instance=club),
                "contact_form": ClubContactForm(instance=club),
                "post_form": ClubPostForm(),
                "comment_form": ClubPostCommentForm(),
                "event_form": ClubEventForm(),
                "resource_form": ClubResourceForm(),
            }
        )
        return context


# Acciones basicas de membresia.
@require_POST
def join_club_view(request, slug):
    """Solicita la incorporacion del usuario autenticado a un club publicado."""

    if not request.user.is_authenticated:
        return JsonResponse({"ok": False, "requires_login": True}, status=401)

    club = get_published_club(slug)
    membership = request_membership(club=club, user=request.user)
    club.refresh_from_db()

    if request.headers.get("x-requested-with") != "XMLHttpRequest":
        messages.success(request, f"Ya formas parte de {club.name}.")
        return redirect("clubs:detail", slug=club.slug)

    return JsonResponse(
        {
            "ok": True,
            "status": membership.status,
            "button_label": "Ya eres miembro",
            "detail_url": reverse("clubs:detail", kwargs={"slug": club.slug}),
            "members_count": club.active_members_count,
        }
    )


@require_POST
@login_required
def leave_club_view(request, slug):
    """Da de baja al usuario actual de un club activo."""

    club = get_published_club(slug)
    membership = club.memberships.filter(
        user=request.user,
        status=ClubMembership.Status.APPROVED,
        left_at__isnull=True,
    ).first()

    if membership:
        membership.status = ClubMembership.Status.CANCELLED
        membership.left_at = timezone.now()
        membership.removal_reason = ClubMembership.RemovalReason.VOLUNTARY_LEAVE
        membership.removal_reason_other = ""
        membership.save(update_fields=["status", "left_at", "removal_reason", "removal_reason_other"])
        messages.success(request, f"Te has dado de baja de {club.name}.")
    return redirect("clubs:detail", slug=club.slug)


# Formularios de gestion general.
@require_POST
@login_required
def update_general_view(request, slug):
    """Actualiza la informacion general de un club desde su panel de gestion."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para editar este club.")

    form = ClubGeneralForm(request.POST, request.FILES, instance=club)
    if form.is_valid():
        form.save()
        messages.success(request, "Ficha general actualizada.")
    else:
        messages.error(request, "No se pudo actualizar la ficha general.")
    return redirect("clubs:detail", slug=club.slug)


@require_POST
@login_required
def update_contact_view(request, slug):
    """Actualiza los datos de contacto visibles del club."""

    club = get_published_club(slug)
    if not user_can_manage_club(request.user, club):
        return HttpResponseForbidden("No tienes permisos para editar este club.")

    form = ClubContactForm(request.POST, instance=club)
    if form.is_valid():
        form.save()
        messages.success(request, "Contacto actualizado.")
    else:
        messages.error(request, "No se pudo actualizar el contacto.")
    return redirect("clubs:detail", slug=club.slug)
