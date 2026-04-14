"""Punto de entrada unificado para las vistas del modulo de clubes."""

# Vistas publicas y de detalle.
from .views_public import (
    ClubDetailView,
    ClubListView,
    join_club_view,
    leave_club_view,
    update_contact_view,
    update_general_view,
)

# Vistas de gestion de miembros.
from .views_memberships import remove_member_view, update_member_role_view

# Vistas de encuestas.
from .views_polls import close_poll_view, create_poll_view, delete_poll_view, vote_poll_view

# Vistas de publicaciones.
from .views_posts import (
    comment_post_view,
    create_post_view,
    delete_comment_view,
    delete_post_view,
    like_post_view,
    update_post_view,
)

# Vistas de eventos.
from .views_events import (
    create_event_view,
    delete_event_attendance_view,
    delete_event_view,
    join_event_view,
    update_event_attendance_view,
    update_event_view,
)

# Vistas de recursos compartidos.
from .views_resources import delete_resource_view, upload_resource_view


__all__ = [
    "ClubDetailView",
    "ClubListView",
    "close_poll_view",
    "comment_post_view",
    "create_event_view",
    "create_poll_view",
    "create_post_view",
    "delete_comment_view",
    "delete_event_attendance_view",
    "delete_event_view",
    "delete_poll_view",
    "delete_post_view",
    "delete_resource_view",
    "join_club_view",
    "join_event_view",
    "leave_club_view",
    "like_post_view",
    "remove_member_view",
    "update_contact_view",
    "update_event_attendance_view",
    "update_event_view",
    "update_general_view",
    "update_member_role_view",
    "update_post_view",
    "upload_resource_view",
    "vote_poll_view",
]
