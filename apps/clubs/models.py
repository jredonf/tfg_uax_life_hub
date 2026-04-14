from django.conf import settings
from django.db import models
from django.utils.text import slugify


class ClubCategory(models.Model):
    """Agrupa los clubes por temática para facilitar su navegación."""

    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    image = models.ImageField(upload_to="clubs/categories/", blank=True, null=True)
    # Descripción visible de la categoría en listados y detalle.
    description = models.TextField(blank=True)
    # Orden manual para destacar categorías en la interfaz.
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "name")
        verbose_name = "Categoría de club"
        verbose_name_plural = "Categorías de club"

    def save(self, *args, **kwargs):
        # Genera el slug automáticamente la primera vez que se guarda la categoría.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Club(models.Model):
    """Representa un club universitario con su información y estado operativo."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Borrador"
        PUBLISHED = "published", "Publicado"
        CLOSED = "closed", "Cerrado"
        ARCHIVED = "archived", "Archivado"

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    image = models.ImageField(upload_to="clubs/images/", blank=True, null=True)
    # Resumen breve mostrado en tarjetas y listados.
    short_description = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    # Categoría principal del club para clasificación y filtrado.
    category = models.ForeignKey(
        ClubCategory,
        on_delete=models.PROTECT,
        related_name="clubs",
    )
    # Relación de miembros gestionada mediante el modelo intermedio de membresía.
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ClubMembership",
        through_fields=("club", "user"),
        related_name="joined_clubs",
        blank=True,
    )
    campus = models.CharField(max_length=100, blank=True)
    rules = models.TextField(blank=True)
    # Canales de contacto y apoyo visual del club.
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=40, blank=True)
    contact_url = models.URLField(blank=True)
    cover_image = models.ImageField(upload_to="clubs/covers/", blank=True, null=True)
    logo_image = models.ImageField(upload_to="clubs/logos/", blank=True, null=True)
    # Capacidad y estado editorial del club dentro de la plataforma.
    capacity = models.PositiveIntegerField(default=0)
    current_status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
    )
    requires_approval = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)

    def save(self, *args, **kwargs):
        # Genera un slug estable si todavía no existe.
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    @property
    def active_members_count(self):
        # Reutiliza una anotación previa si existe para evitar consultas adicionales.
        annotated_count = getattr(self, "active_members_total", None)
        if annotated_count is not None:
            return annotated_count

        # Cuenta solo membresías aprobadas y actualmente activas.
        return self.memberships.filter(
            status=ClubMembership.Status.APPROVED,
            left_at__isnull=True,
        ).count()

    @property
    def approved_memberships_count(self):
        return self.active_members_count

    @property
    def available_slots(self):
        # Nunca devuelve plazas negativas aunque se supere la capacidad teórica.
        return max(self.capacity - self.active_members_count, 0)


class ClubMembership(models.Model):
    """Modela la relación de pertenencia entre un usuario y un club."""

    class RoleInClub(models.TextChoices):
        MEMBER = "member", "Miembro"
        CAPTAIN = "captain", "Capitán"
        MANAGER = "manager", "Responsable"
        ADMIN = "admin", "Administrador"

    class Status(models.TextChoices):
        PENDING = "pending", "Pendiente"
        APPROVED = "approved", "Aprobada"
        REJECTED = "rejected", "Rechazada"
        CANCELLED = "cancelled", "Cancelada"

    class RemovalReason(models.TextChoices):
        VOLUNTARY_LEAVE = "voluntary_leave", "Baja Voluntaria"
        FINISHED_STUDIES = "finished_studies", "Finalizó estudios universitarios"
        LOW_ATTENDANCE = "low_attendance", "Poca asistencia"
        BAD_BEHAVIOR = "bad_behavior", "Mal comportamiento"
        OTHER = "other", "Otros"

    # Club al que pertenece la membresía.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="memberships")
    # Usuario asociado a la membresía del club.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="club_memberships",
    )
    # Rol desempeñado y estado administrativo de la solicitud o membresía.
    role_in_club = models.CharField(
        max_length=20,
        choices=RoleInClub.choices,
        default=RoleInClub.MEMBER,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(blank=True, null=True)
    # Motivo normalizado de salida cuando una membresía finaliza.
    removal_reason = models.CharField(
        max_length=40,
        choices=RemovalReason.choices,
        blank=True,
    )
    removal_reason_other = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = ("club", "user")
        ordering = ("-joined_at",)

    def __str__(self):
        return f"{self.user} - {self.club}"

class ClubPost(models.Model):
    """Publicación interna generada por un club para su comunidad."""

    # Club al que pertenece la publicación.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="posts")
    # Autor responsable del contenido publicado.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_posts")
    title = models.CharField(max_length=150)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="clubs/posts/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class ClubPostComment(models.Model):
    """Comentario realizado por un usuario sobre una publicación de club."""

    # Publicación comentada dentro del muro del club.
    post = models.ForeignKey(ClubPost, on_delete=models.CASCADE, related_name="comments")
    # Usuario que escribe el comentario.
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_post_comments")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)

    def __str__(self):
        return f"Comentario de {self.author} en {self.post}"


class ClubPostLike(models.Model):
    """Registra que un usuario ha marcado una publicación con un me gusta."""

    # Publicación valorada positivamente por el usuario.
    post = models.ForeignKey(ClubPost, on_delete=models.CASCADE, related_name="likes")
    # Usuario que emite la reacción.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_post_likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user} - {self.post}"


class ClubResource(models.Model):
    """Almacena recursos compartidos por un club para sus miembros."""

    # Club propietario del recurso subido a la plataforma.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="resources")
    # Usuario que sube y mantiene el recurso.
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_resources")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="clubs/resources/")
    # Descripción opcional para contextualizar el recurso.
    description = models.TextField(blank=True, max_length=600)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    @property
    def is_image(self):
        # Determina si el archivo puede tratarse como imagen para la vista previa.
        return self.file.name.lower().endswith((".jpg", ".jpeg", ".png", ".gif", ".webp", ".avif"))


class ClubPoll(models.Model):
    """Representa una votación creada por un club para recoger decisiones."""

    class Status(models.TextChoices):
        ACTIVE = "active", "Activa"
        CLOSED = "closed", "Cerrada"

    class Visibility(models.TextChoices):
        PUBLIC = "public", "Pública"
        PRIVATE = "private", "Privada"

    # Club organizador de la encuesta o votación.
    club = models.ForeignKey(Club, on_delete=models.CASCADE, related_name="polls")
    # Usuario que crea la votación.
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_polls")
    title = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    # Parámetros de visibilidad y ciclo de vida de la votación.
    visibility = models.CharField(
        max_length=20,
        choices=Visibility.choices,
        default=Visibility.PRIVATE,
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    closes_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self):
        return self.title

    @property
    def is_open(self):
        from django.utils import timezone

        # Una votación solo está abierta si sigue activa y no ha vencido.
        if self.status != self.Status.ACTIVE:
            return False
        return not self.closes_at or timezone.now() <= self.closes_at


class ClubPollOption(models.Model):
    """Define una opción seleccionable dentro de una votación de club."""

    # Votación a la que pertenece la opción.
    poll = models.ForeignKey(ClubPoll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=100)
    # Orden configurable para presentar las opciones al usuario.
    display_order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("display_order", "id")

    def __str__(self):
        return self.text


class ClubPollVote(models.Model):
    """Registra el voto emitido por un usuario en una votación concreta."""

    # Votación en la que participa el usuario.
    poll = models.ForeignKey(ClubPoll, on_delete=models.CASCADE, related_name="votes")
    # Opción elegida dentro de la votación.
    option = models.ForeignKey(ClubPollOption, on_delete=models.CASCADE, related_name="votes")
    # Usuario que emite el voto.
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="club_poll_votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("poll", "user")
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.user} - {self.poll}"
