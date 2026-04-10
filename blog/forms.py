from django import forms
from django.utils import timezone

from .models import Article


class ArticleForm(forms.ModelForm):
    date_publication = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M"],
        widget=forms.DateTimeInput(
            format="%Y-%m-%dT%H:%M",
            attrs={"type": "datetime-local"},
        ),
        initial=timezone.localtime().replace(second=0, microsecond=0),
    )

    class Meta:
        model = Article
        fields = ["titre", "contenu", "statut", "date_publication", "image"]
        widgets = {
            "titre": forms.TextInput(attrs={"placeholder": "Titre de l'article"}),
            "contenu": forms.Textarea(
                attrs={
                    "rows": 10,
                    "placeholder": "Redigez ici le contenu de votre article",
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
        self.fields["image"].widget.attrs.update({"accept": "image/*"})
        if self.instance.pk and self.instance.date_publication:
            self.initial["date_publication"] = timezone.localtime(
                self.instance.date_publication
            ).strftime("%Y-%m-%dT%H:%M")
