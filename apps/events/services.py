from django.conf import settings
from django.core.mail import send_mail


def send_contact_request_notification(contact_request):
    """Envía por correo la consulta al email administrador configurado."""

    if not settings.ADMIN_CONTACT_EMAIL:
        return False

    query_type_label = contact_request.get_query_type_display()
    subject = f"[UAX Life Hub] Nueva consulta: {query_type_label}"
    message = "\n".join(
        [
            "Se ha recibido una nueva consulta desde el formulario de contacto.",
            "",
            f"Nombre: {contact_request.name}",
            f"Correo: {contact_request.email}",
            f"Tipo de consulta: {query_type_label}",
            f"Tema específico: {contact_request.query_topic}",
            f"Fecha de envío: {contact_request.submitted_at:%d/%m/%Y %H:%M}",
            "",
            "Mensaje:",
            contact_request.message,
        ]
    )

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_CONTACT_EMAIL],
        fail_silently=False,
    )
    return True
