from django.views.generic import TemplateView


class ContactPageView(TemplateView):
    """Muestra la página pública del formulario de contacto."""

    template_name = "contact/contact_page.html"
