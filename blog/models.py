from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone


class StatutPublication(models.TextChoices):
    BROUILLON = "draft", "Brouillon"
    PUBLIE = "published", "Publie"


class Article(models.Model):
    titre = models.CharField(max_length=200)
    contenu = models.TextField()
    date_publication = models.DateTimeField(default=timezone.now)
    auteur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="articles",
    )
    image = models.ImageField(upload_to="articles/", blank=True, null=True)
    statut = models.CharField(
        max_length=10,
        choices=StatutPublication.choices,
        default=StatutPublication.BROUILLON,
    )
    cree_le = models.DateTimeField(auto_now_add=True)
    mis_a_jour_le = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-date_publication", "-cree_le")
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.titre

    def get_absolute_url(self):
        return reverse("blog:article_detail", kwargs={"pk": self.pk})

    @property
    def est_publie(self):
        return self.statut == StatutPublication.PUBLIE

