from django.db import models


class HomePageSettings(models.Model):
    """Centraliza la configuración editable de la portada principal."""

    # Titular principal mostrado en la cabecera de la página inicial.
    hero_title = models.CharField(max_length=200, default="DEPORTE UNIVERSITARIO UAX")
    # Texto descriptivo de apoyo para comunicar la propuesta de valor.
    hero_description = models.TextField(
        default=(
            "Desarrollo deportivo universitario.\n"
            "Instalaciones de alto rendimiento.\n"
            "Participa en ligas internas y clubes."
        )
    )
    # Textos del botón principal según el estado de autenticación del usuario.
    hero_button_text_logged_out = models.CharField(max_length=80, default="Iniciar sesión")
    hero_button_text_logged_in = models.CharField(max_length=80, default="Explorar clubes")
    # Imagen destacada usada en la portada.
    hero_image = models.ImageField(upload_to="core/home/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Configuracion de la home"
        verbose_name_plural = "Configuracion de la home"

    def __str__(self):
        # Texto legible usado al representar la configuración en código y depuración.
        return "Configuración de la home"
