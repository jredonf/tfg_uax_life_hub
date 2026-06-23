from django import forms

from apps.clubs.models import Club

from .models import ContactRequest


CONTACT_INPUT_ATTRS = {
    "class": "contact-form__input",
}


class ContactRequestForm(forms.ModelForm):
    """Recoge consultas públicas desde la página de contacto."""

    query_topic = forms.ChoiceField(
        label="Tema específico",
        choices=(),
        widget=forms.Select(
            attrs={
                **CONTACT_INPUT_ATTRS,
                "data-query-topic-select": "true",
            }
        ),
    )
    accepted_privacy = forms.BooleanField(
        label="He leído y acepto el tratamiento de mis datos para gestionar esta consulta.",
        required=True,
        error_messages={
            "required": "Debes aceptar la política de privacidad para enviar la consulta.",
        },
    )

    class Meta:
        model = ContactRequest
        fields = ("name", "email", "query_type", "query_topic", "message", "accepted_privacy")
        labels = {
            "name": "Nombre",
            "email": "Correo electrónico",
            "query_type": "Tipo de consulta",
            "message": "Mensaje",
        }
        widgets = {
            "name": forms.TextInput(
                attrs={
                    **CONTACT_INPUT_ATTRS,
                    "autocomplete": "name",
                    "placeholder": "Introduce tu nombre",
                    "maxlength": 120,
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    **CONTACT_INPUT_ATTRS,
                    "autocomplete": "email",
                    "placeholder": "Introduce tu correo electrónico",
                }
            ),
            "query_type": forms.Select(
                attrs={
                    **CONTACT_INPUT_ATTRS,
                    "data-query-type-select": "true",
                }
            ),
            "message": forms.Textarea(
                attrs={
                    **CONTACT_INPUT_ATTRS,
                    "rows": 6,
                    "maxlength": 1500,
                    "placeholder": "Escribe aquí tu mensaje",
                }
            ),
            "accepted_privacy": forms.CheckboxInput(attrs={"class": "contact-form__checkbox"}),
        }
        help_texts = {
            "message": "Máximo 1500 caracteres.",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.query_topic_groups = self.build_query_topic_groups()
        selected_query_type = self.get_selected_query_type()
        self.fields["query_topic"].choices = self.get_query_topic_choices(selected_query_type)
        if selected_query_type:
            self.fields["query_topic"].widget.attrs.pop("disabled", None)
        else:
            self.fields["query_topic"].widget.attrs["disabled"] = "disabled"

    def build_query_topic_groups(self):
        """Agrupa las opciones del segundo desplegable según el tipo de consulta."""

        published_clubs = list(
            Club.objects.filter(current_status=Club.Status.PUBLISHED)
            .order_by("name")
            .values_list("slug", "name")
        )
        return {
            ContactRequest.QueryType.CLUBS_ASSOCIATIONS: published_clubs,
            ContactRequest.QueryType.FITNESS_CENTER: [
                ("gym", "Gimnasio"),
                ("tennis_padel_schools", "Escuelas de tenis y pádel"),
                ("golf_club", "Club de Golf"),
            ],
            ContactRequest.QueryType.INTERNAL_LEAGUES: [
                ("coming_soon", "Próximamente"),
            ],
            ContactRequest.QueryType.COMPETITION_TEAMS: [
                ("coming_soon", "Próximamente"),
            ],
            ContactRequest.QueryType.INDIVIDUAL_SPORTS: [
                ("coming_soon", "Próximamente"),
            ],
            ContactRequest.QueryType.TECHNICAL_SERVICE: [
                ("technical_issue", "Incidencia técnica"),
                ("suggestions", "Sugerencias"),
                ("other", "Otros"),
            ],
        }

    def get_selected_query_type(self):
        """Recupera el tipo de consulta actual para precargar el segundo select."""

        if self.is_bound:
            return self.data.get(self.add_prefix("query_type"), "")
        if self.initial.get("query_type"):
            return self.initial["query_type"]
        if self.instance and self.instance.pk:
            return self.instance.query_type
        return ""

    def get_query_topic_choices(self, query_type):
        """Construye las opciones visibles del selector dependiente."""

        base_choices = [("", "Selecciona una opción")]
        if not query_type:
            return base_choices
        return base_choices + self.query_topic_groups.get(query_type, [])

    def clean(self):
        """Valida que el tema elegido pertenezca al tipo de consulta seleccionado."""

        cleaned_data = super().clean()
        query_type = cleaned_data.get("query_type")
        query_topic = cleaned_data.get("query_topic")

        valid_choices = {
            value
            for value, _label in self.query_topic_groups.get(query_type, [])
        }
        if query_type and query_topic and query_topic not in valid_choices:
            self.add_error(
                "query_topic",
                "Selecciona una opción válida para el tipo de consulta indicado.",
            )

        return cleaned_data
