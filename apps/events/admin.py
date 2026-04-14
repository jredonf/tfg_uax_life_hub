from django.contrib import admin

from .models import ClubEvent, ClubEventAttendance


@admin.register(ClubEvent)
class ClubEventAdmin(admin.ModelAdmin):
    """Administracion de eventos organizados por los clubes."""

    list_display = ("title", "club", "start_datetime", "location")


@admin.register(ClubEventAttendance)
class ClubEventAttendanceAdmin(admin.ModelAdmin):
    """Consulta de asistencias registradas para cada evento."""

    list_display = ("event", "user", "companions_count", "joined_at")
    search_fields = ("event__title", "user__username", "user__email")
