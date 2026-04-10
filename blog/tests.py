from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Article, StatutPublication


User = get_user_model()


class ArticleViewsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="MotDePasse123!",
        )
        self.visiteur = User.objects.create_user(
            username="visiteur",
            email="visiteur@example.com",
            password="MotDePasse123!",
        )
        self.article_publie = Article.objects.create(
            titre="Article publie",
            contenu="Contenu public",
            statut=StatutPublication.PUBLIE,
            date_publication=timezone.now(),
            auteur=self.admin,
        )
        self.brouillon = Article.objects.create(
            titre="Article brouillon",
            contenu="Contenu prive",
            statut=StatutPublication.BROUILLON,
            date_publication=timezone.now(),
            auteur=self.admin,
        )

    def test_public_list_shows_only_published_articles(self):
        response = self.client.get(reverse("blog:article_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.article_publie.titre)
        self.assertNotContains(response, self.brouillon.titre)

    def test_staff_list_shows_all_articles(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("blog:article_list"))

        self.assertContains(response, self.article_publie.titre)
        self.assertContains(response, self.brouillon.titre)

    def test_public_cannot_access_draft_detail(self):
        response = self.client.get(
            reverse("blog:article_detail", kwargs={"pk": self.brouillon.pk})
        )

        self.assertEqual(response.status_code, 404)

    def test_staff_can_create_article(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            reverse("blog:article_create"),
            {
                "titre": "Nouveau billet",
                "contenu": "Texte complet",
                "statut": StatutPublication.PUBLIE,
                "date_publication": timezone.now().strftime("%Y-%m-%dT%H:%M"),
            },
        )

        self.assertEqual(response.status_code, 302)
        article = Article.objects.get(titre="Nouveau billet")
        self.assertEqual(article.auteur, self.admin)

    def test_non_staff_cannot_access_create_view(self):
        self.client.force_login(self.visiteur)

        response = self.client.get(reverse("blog:article_create"))

        self.assertEqual(response.status_code, 403)

    def test_staff_can_logout_from_blog_route(self):
        self.client.force_login(self.admin)

        response = self.client.post(reverse("blog:logout"), follow=True)

        self.assertEqual(response.status_code, 200)
        self.assertFalse("_auth_user_id" in self.client.session)


class SeedBlogDemoCommandTests(TestCase):
    def test_seed_command_creates_demo_admin_and_articles(self):
        call_command("seed_blog_demo")

        admin = User.objects.get(username="admin")
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertTrue(admin.check_password("AdminMicda2026!"))
        self.assertEqual(Article.objects.count(), 2)
