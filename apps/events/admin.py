from django.contrib import admin

from .models import ClubEvent, ClubEventAttendance, ContactRequest


@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    """Administracion de eventos organizados por los clubes."""

    list_display = ("title", "club", "start_datetime", "location")


@admin.register(ClubEventAttendance)
class ClubEventAttendanceAdmin(admin.ModelAdmin):
    """Consulta de asistencias registradas para cada evento."""

    list_display = ("event", "user", "companions_count", "joined_at")
    search_fields = ("event__title", "user__username", "user__email")


@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    """Consulta de mensajes enviados desde el formulario público."""

    list_display = ("query_topic", "name", "email", "query_type", "submitted_at")
    list_filter = ("query_type", "submitted_at")
    search_fields = ("query_topic", "name", "email", "message")
