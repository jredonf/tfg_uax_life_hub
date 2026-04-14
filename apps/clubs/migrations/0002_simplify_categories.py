from django.db import migrations
from django.utils.text import slugify


def simplify_categories(apps, schema_editor):
    Club = apps.get_model("clubs", "Club")
    ClubCategory = apps.get_model("clubs", "ClubCategory")

    category_specs = {
        "Social": {
            "slug": "social",
            "description": "Clubes culturales, sociales, multiculturales y de comunidad.",
            "display_order": 1,
        },
        "Desarrollo Profesional": {
            "slug": "desarrollo-profesional",
            "description": "Clubes de tecnologia, empresa, liderazgo, derecho y desarrollo profesional.",
            "display_order": 2,
        },
        "Sostenibilidad y Naturaleza": {
            "slug": "sostenibilidad-y-naturaleza",
            "description": "Clubes de sostenibilidad, entorno natural y actividades al aire libre.",
            "display_order": 3,
        },
        "Clubes Deportivos": {
            "slug": "clubes-deportivos",
            "description": "Clubes y disciplinas deportivas universitarias.",
            "display_order": 4,
        },
    }

    repurpose_map = {
        "Social": "Social",
        "Business": "Desarrollo Profesional",
        "Naturaleza": "Sostenibilidad y Naturaleza",
        "Deporte": "Clubes Deportivos",
    }

    categories = {}
    for source_name, target_name in repurpose_map.items():
        category = ClubCategory.objects.filter(name=source_name).first()
        if category:
            spec = category_specs[target_name]
            category.name = target_name
            category.slug = spec["slug"]
            category.description = spec["description"]
            category.display_order = spec["display_order"]
            category.save(update_fields=["name", "slug", "description", "display_order"])
            categories[target_name] = category

    for target_name, spec in category_specs.items():
        if target_name not in categories:
            categories[target_name] = ClubCategory.objects.create(
                name=target_name,
                slug=spec["slug"],
                description=spec["description"],
                display_order=spec["display_order"],
            )

    club_category_map = {
        "Teatro": "Social",
        "Fotografia": "Social",
        "Musica": "Social",
        "Ajedrez": "Social",
        "Cine": "Social",
        "Videojuegos": "Social",
        "African Student Association": "Social",
        "Aeroespacial": "Desarrollo Profesional",
        "Formula Student": "Desarrollo Profesional",
        "Debate": "Desarrollo Profesional",
        "Finanzas": "Desarrollo Profesional",
        "Emprendimiento": "Desarrollo Profesional",
        "UAX Connect": "Desarrollo Profesional",
        "Ciberseguridad": "Desarrollo Profesional",
        "ELSA": "Desarrollo Profesional",
        "Ganaderia": "Sostenibilidad y Naturaleza",
        "Montana": "Sostenibilidad y Naturaleza",
        "Bicicleta": "Sostenibilidad y Naturaleza",
        "Futbol 11": "Clubes Deportivos",
        "Futbol Sala": "Clubes Deportivos",
        "Rugby": "Clubes Deportivos",
        "Voleibol": "Clubes Deportivos",
        "Baloncesto": "Clubes Deportivos",
        "Atletismo": "Clubes Deportivos",
    }

    for club in Club.objects.select_related("category"):
        target_name = club_category_map.get(club.name)

        if target_name is None:
            if club.club_type == "sports":
                target_name = "Clubes Deportivos"
            elif club.category.name in ("Naturaleza", "Sostenibilidad y Naturaleza"):
                target_name = "Sostenibilidad y Naturaleza"
            elif club.category.name in ("Business", "Tecnologia", "Liderazgo", "Legal", "Desarrollo Profesional"):
                target_name = "Desarrollo Profesional"
            else:
                target_name = "Social"

        club.category = categories[target_name]
        club.save(update_fields=["category"])

    ClubCategory.objects.exclude(id__in=[category.id for category in categories.values()]).delete()

    for target_name, category in categories.items():
        spec = category_specs[target_name]
        if not category.slug:
            category.slug = slugify(category.name)
        category.description = spec["description"]
        category.display_order = spec["display_order"]
        category.save(update_fields=["slug", "description", "display_order"])


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ("clubs", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(simplify_categories, migrations.RunPython.noop),
        migrations.RemoveField(
            model_name="clubcategory",
            name="category_type",
        ),
    ]
