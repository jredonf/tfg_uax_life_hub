from django.contrib import admin

from .models import (
    Club,
    ClubCategory,
    ClubMembership,
    ClubPoll,
    ClubPollOption,
    ClubPollVote,
    ClubPost,
    ClubPostComment,
    ClubPostLike,
    ClubResource,
)


class ClubMembershipInline(admin.TabularInline):
    """Permite gestionar membresías directamente desde la ficha del club."""

    model = ClubMembership
    extra = 0
    autocomplete_fields = ("user",)
    fields = ("user", "role_in_club", "status", "joined_at", "left_at")
    readonly_fields = ("joined_at",)


class ClubPollOptionInline(admin.TabularInline):
    """Facilita editar las opciones de una encuesta desde su propio formulario."""

    model = ClubPollOption
    extra = 2


@admin.register(ClubCategory)
class ClubCategoryAdmin(admin.ModelAdmin):
    """Administración de categorías para clasificar los clubes."""

    list_display = ("name", "display_order")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
    fields = ("name", "slug", "image", "description", "display_order")


@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    """Panel de administración principal para clubes universitarios."""

    list_display = ("name", "category", "active_members_count_display", "capacity", "current_status")
    list_filter = ("current_status", "category")
    search_fields = ("name", "short_description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = (ClubMembershipInline,)
    fields = (
        "name",
        "slug",
        "image",
        "cover_image",
        "logo_image",
        "short_description",
        "description",
        "category",
        "campus",
        "rules",
        "contact_email",
        "contact_phone",
        "contact_url",
        "capacity",
        "current_status",
        "requires_approval",
    )

    @admin.display(description="Miembros activos")
    def active_members_count_display(self, obj):
        # Reutiliza la propiedad del modelo para mostrar el total consolidado.
        return obj.active_members_count


@admin.register(ClubMembership)
class ClubMembershipAdmin(admin.ModelAdmin):
    """Administración individual de membresías y roles dentro del club."""

    list_display = ("club", "user", "role_in_club", "status", "joined_at")
    list_filter = ("status", "role_in_club")
    search_fields = ("club__name", "user__username", "user__email")

@admin.register(ClubPost)
class ClubPostAdmin(admin.ModelAdmin):
    """Gestión administrativa de publicaciones internas de los clubes."""

    list_display = ("title", "club", "author", "created_at")
    list_filter = ("club",)
    search_fields = ("title", "body", "club__name", "author__username")


@admin.register(ClubPostComment)
class ClubPostCommentAdmin(admin.ModelAdmin):
    """Consulta y moderación de comentarios sobre publicaciones."""

    list_display = ("post", "author", "created_at")
    search_fields = ("post__title", "author__username", "body")


@admin.register(ClubPostLike)
class ClubPostLikeAdmin(admin.ModelAdmin):
    """Visualización de reacciones positivas sobre publicaciones."""

    list_display = ("post", "user", "created_at")
    search_fields = ("post__title", "user__username")


@admin.register(ClubResource)
class ClubResourceAdmin(admin.ModelAdmin):
    """Gestion de archivos y recursos compartidos por los clubes."""

    list_display = ("title", "club", "uploaded_by", "created_at")
    search_fields = ("title", "description", "club__name", "uploaded_by__username")


@admin.register(ClubPoll)
class ClubPollAdmin(admin.ModelAdmin):
    """Administracion de encuestas y votaciones creadas por los clubes."""

    list_display = ("title", "club", "visibility", "status", "created_by", "created_at")
    list_filter = ("club", "visibility", "status")
    search_fields = ("title", "description", "club__name", "created_by__username")
    inlines = (ClubPollOptionInline,)


@admin.register(ClubPollVote)
class ClubPollVoteAdmin(admin.ModelAdmin):
    """Consulta administrativa de votos emitidos por los usuarios."""

    list_display = ("poll", "option", "user", "created_at")
    list_filter = ("poll__club",)
    search_fields = ("poll__title", "option__text", "user__username")
