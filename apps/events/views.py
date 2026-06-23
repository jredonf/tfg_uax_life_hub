from smtplib import SMTPException

from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import FormView

from .forms import ContactRequestForm
from .services import send_contact_request_notification


class ContactPageView(FormView):
    """Muestra la página pública del formulario de contacto."""

    template_name = "contact/contact_page.html"
    form_class = ContactRequestForm
    success_url = reverse_lazy("contact:page")

    def form_valid(self, form):
        # Guarda la consulta y notifica por correo al administrador si está configurado.
        contact_request = form.save()
        try:
            email_sent = send_contact_request_notification(contact_request)
        except SMTPException:
            email_sent = False
        except OSError:
            email_sent = False

        if email_sent:
            messages.success(self.request, "Tu consulta se ha enviado correctamente.")
        else:
            messages.success(
                self.request,
                "Tu consulta se ha guardado correctamente. Revisa la configuración de correo para activar el aviso automático.",
            )
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        # Expone el mapa de temas dependientes al template.
        context = super().get_context_data(**kwargs)
        context["query_topic_groups"] = context["form"].query_topic_groups
        return context
