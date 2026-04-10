from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from blog.models import Article, StatutPublication


class Command(BaseCommand):
    help = "Cree un compte administrateur de demonstration et des articles exemples."

    def handle(self, *args, **options):
        user_model = get_user_model()
        admin, created = user_model.objects.get_or_create(
            username="admin",
            defaults={
                "email": "admin@micda.local",
                "first_name": "Admin",
                "last_name": "MICDA",
                "is_staff": True,
                "is_superuser": True,
            },
        )

        admin.email = "admin@micda.local"
        admin.first_name = "Admin"
        admin.last_name = "MICDA"
        admin.is_staff = True
        admin.is_superuser = True
        admin.set_password("AdminMicda2026!")
        admin.save()

        now = timezone.now()

        article_public, _ = Article.objects.get_or_create(
            titre="Bienvenue sur le blog MICDA",
            defaults={
                "contenu": (
                    "Ce blog de demonstration permet de tester la liste des articles, "
                    "le detail d un article, l interface d administration Django, "
                    "ainsi que le CRUD complet en Class-Based Views."
                ),
                "statut": StatutPublication.PUBLIE,
                "date_publication": now,
                "auteur": admin,
            },
        )

        article_brouillon, _ = Article.objects.get_or_create(
            titre="Article en preparation",
            defaults={
                "contenu": (
                    "Cet article est un brouillon de demonstration. "
                    "Il doit etre visible uniquement pour l administrateur."
                ),
                "statut": StatutPublication.BROUILLON,
                "date_publication": now,
                "auteur": admin,
            },
        )

        self.stdout.write(
            self.style.SUCCESS(
                "Jeu de demonstration pret : "
                f"admin={'cree' if created else 'mis a jour'}, "
                f"articles={[article_public.titre, article_brouillon.titre]}"
            )
        )
