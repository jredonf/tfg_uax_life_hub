from django import forms

from apps.events.models import ClubEvent

from .models import Club, ClubMembership, ClubPoll, ClubPost, ClubPostComment, ClubResource
from .rich_text import sanitize_rich_text


class ClubJoinForm(forms.ModelForm):
    """Formulario mínimo para representar una solicitud de alta en un club."""

    class Meta:
        model = ClubMembership
        fields = []


class ClubGeneralForm(forms.ModelForm):
    """Gestiona la información descriptiva principal del club."""

    class Meta:
        model = Club
        fields = ("image", "description", "rules")
        labels = {
            "image": "Imagen",
            "description": "Descripción",
            "rules": "Normas del club",
        }
        widgets = {
            "description": forms.Textarea(attrs={"data-rich-editor": "true", "rows": 6}),
            "rules": forms.Textarea(attrs={"data-rich-editor": "true", "rows": 6}),
        }

    def clean_description(self):
        # Sanea el contenido enriquecido antes de persistirlo.
        return sanitize_rich_text(self.cleaned_data["description"])

    def clean_rules(self):
        # Reutiliza el mismo saneado para las normas visibles del club.
        return sanitize_rich_text(self.cleaned_data["rules"])


class ClubContactForm(forms.ModelForm):
    """Edita los canales de contacto y localización del club."""

    class Meta:
        model = Club
        fields = ("contact_email", "contact_phone", "contact_url", "campus")
        labels = {
            "contact_email": "Correo de contacto",
            "contact_phone": "Teléfono",
            "contact_url": "Enlace de contacto",
            "campus": "Campus",
        }


class ClubPostForm(forms.ModelForm):
    """Formulario de publicación de noticias o comunicados del club."""

    class Meta:
        model = ClubPost
        fields = ("title", "body", "image")
        labels = {
            "title": "Título",
            "body": "Texto",
            "image": "Imagen",
        }
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 150}),
            "body": forms.Textarea(attrs={"data-rich-editor": "true", "rows": 7}),
        }
        help_texts = {
            "title": "Máximo 150 caracteres.",
        }

    def clean_body(self):
        # Limpia el HTML enriquecido para mantener un contenido seguro.
        return sanitize_rich_text(self.cleaned_data["body"])


class ClubPostCommentForm(forms.ModelForm):
    """Recoge comentarios breves sobre publicaciones del club."""

    body = forms.CharField(
        label="Comentario",
        max_length=500,
        widget=forms.Textarea(
            attrs={
                "maxlength": 500,
                "rows": 2,
                "placeholder": "Escribe un comentario...",
            }
        ),
        error_messages={
            "max_length": "El comentario no puede superar los 500 caracteres.",
        },
    )

    class Meta:
        model = ClubPostComment
        fields = ("body",)


class ClubEventForm(forms.ModelForm):
    """Formulario para crear y editar eventos del club."""

    description = forms.CharField(
        label="Descripción",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "maxlength": 500}),
        error_messages={
            "max_length": "La descripción no puede superar los 500 caracteres.",
        },
    )

    class Meta:
        model = ClubEvent
        fields = ("title", "description", "start_datetime", "end_datetime", "capacity", "location", "location_url")
        labels = {
            "title": "Título",
            "description": "Descripción",
            "start_datetime": "Fecha y hora de inicio",
            "end_datetime": "Fecha y hora de fin",
            "location": "Ubicación",
            "location_url": "Enlace de ubicación",
            "capacity": "Aforo",
        }
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "start_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "datetime-smart-input",
                    "data-datetime-smart": "true",
                    "title": "Puedes escribir la fecha o abrir el selector desde cualquier zona del campo.",
                }
            ),
            "end_datetime": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "datetime-smart-input",
                    "data-datetime-smart": "true",
                    "title": "Puedes escribir la fecha o abrir el selector desde cualquier zona del campo.",
                }
            ),
            "location_url": forms.URLInput(attrs={"placeholder": "https://maps.google.com/..."}),
            "capacity": forms.NumberInput(attrs={"min": 1}),
        }
        help_texts = {
            "description": "Máximo 500 caracteres.",
            "start_datetime": "Puedes escribir la fecha o pulsar en cualquier zona del campo.",
            "end_datetime": "Opcional. Puedes escribir la fecha o pulsar en cualquier zona del campo.",
            "location_url": "Opcional. Pega aquí un enlace a Maps o a otra ubicación.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ajusta valores por defecto y elimina límites HTML no deseados.
        self.fields["end_datetime"].required = False
        self.fields["capacity"].initial = 50
        self.fields["location_url"].widget.attrs.pop("maxlength", None)

    def clean_capacity(self):
        # El aforo mínimo debe permitir al menos una asistencia.
        capacity = self.cleaned_data["capacity"]
        if capacity < 1:
            raise forms.ValidationError("El aforo debe ser al menos 1.")
        return capacity

    def clean(self):
        # Valida que la fecha de inicio no sea posterior a la de fin del evento.
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get("start_datetime")
        end_datetime = cleaned_data.get("end_datetime")

        if start_datetime and end_datetime and start_datetime > end_datetime:
            self.add_error("end_datetime", "La fecha de fin no puede ser anterior a la fecha de inicio.")

        return cleaned_data


class ClubResourceForm(forms.ModelForm):
    """Gestiona la subida de recursos compartidos por el club."""

    class Meta:
        model = ClubResource
        fields = ("title", "file", "description")
        labels = {
            "title": "Título",
            "file": "Archivo",
            "description": "Descripción",
        }
        help_texts = {
            "title": "Máximo 200 caracteres.",
            "description": "Máximo 600 caracteres.",
        }
        widgets = {
            "title": forms.TextInput(attrs={"maxlength": 200}),
            "description": forms.Textarea(attrs={"maxlength": 600, "rows": 4}),
        }


class ClubPollForm(forms.ModelForm):
    """Construye una encuesta con un número variable de opciones."""

    title = forms.CharField(label="Título", max_length=160)
    description = forms.CharField(
        label="Descripción",
        max_length=500,
        required=False,
        widget=forms.Textarea(attrs={"rows": 3, "maxlength": 500}),
    )
    OPTION_FIELD_NAMES = tuple(f"option_{index}" for index in range(1, 9))

    option_1 = forms.CharField(label="Opción 1", max_length=100)
    option_2 = forms.CharField(label="Opción 2", max_length=100)
    option_3 = forms.CharField(label="Opción 3", max_length=100, required=False)
    option_4 = forms.CharField(label="Opción 4", max_length=100, required=False)
    option_5 = forms.CharField(label="Opción 5", max_length=100, required=False)
    option_6 = forms.CharField(label="Opción 6", max_length=100, required=False)
    option_7 = forms.CharField(label="Opción 7", max_length=100, required=False)
    option_8 = forms.CharField(label="Opción 8", max_length=100, required=False)

    class Meta:
        model = ClubPoll
        fields = ("title", "description", "visibility", "closes_at")
        labels = {
            "visibility": "Visibilidad",
            "closes_at": "Fecha de cierre",
        }
        widgets = {
            "closes_at": forms.DateTimeInput(
                attrs={
                    "type": "datetime-local",
                    "class": "datetime-smart-input",
                    "data-datetime-smart": "true",
                }
            ),
        }
        help_texts = {
            "title": "Máximo 160 caracteres.",
            "description": "Máximo 500 caracteres.",
            "visibility": "Pública: visible para todos. Privada: visible solo para miembros del club.",
            "closes_at": "Opcional. Si la dejas vacía, la encuesta seguirá abierta hasta que la cierres.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["closes_at"].required = False
        # Homogeneiza límites y placeholders para todas las opciones.
        for field_name in self.OPTION_FIELD_NAMES:
            self.fields[field_name].widget.attrs.update(
                {
                    "maxlength": 100,
                    "placeholder": "Texto de la opción",
                }
            )

    def clean(self):
        # Exige un mínimo de dos opciones y evita duplicados por texto.
        cleaned_data = super().clean()
        options = [
            cleaned_data.get(field_name, "").strip()
            for field_name in self.OPTION_FIELD_NAMES
            if cleaned_data.get(field_name, "").strip()
        ]
        if len(options) < 2:
            raise forms.ValidationError("La encuesta debe tener al menos 2 opciones.")
        if len(set(option.lower() for option in options)) != len(options):
            raise forms.ValidationError("Las opciones de la encuesta no pueden estar duplicadas.")
        cleaned_data["options"] = options
        return cleaned_data
