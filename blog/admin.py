from django.contrib import admin
from django.utils.html import format_html

from .models import Article


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ("titre", "auteur", "statut", "date_publication", "cree_le")
    list_filter = ("statut", "date_publication", "auteur")
    search_fields = (
        "titre",
        "contenu",
        "auteur__username",
        "auteur__first_name",
        "auteur__last_name",
    )
    ordering = ("-date_publication",)
    date_hierarchy = "date_publication"
    readonly_fields = ("apercu_image", "cree_le", "mis_a_jour_le")
    fieldsets = (
        ("Contenu", {"fields": ("titre", "contenu")}),
        ("Publication", {"fields": ("statut", "date_publication", "auteur")}),
        ("Illustration", {"fields": ("image", "apercu_image")}),
        ("Suivi", {"fields": ("cree_le", "mis_a_jour_le")}),
    )

    def apercu_image(self, obj):
        if not obj.image:
            return "Aucune image"
        return format_html(
            '<img src="{}" alt="{}" style="max-width: 180px; border-radius: 6px;" />',
            obj.image.url,
            obj.titre,
        )

    apercu_image.short_description = "Apercu"

    def save_model(self, request, obj, form, change):
        if not obj.auteur_id:
            obj.auteur = request.user
        super().save_model(request, obj, form, change)
