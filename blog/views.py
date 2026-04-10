from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import ArticleForm
from .models import Article, StatutPublication


class StaffRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    login_url = reverse_lazy("admin:login")
    redirect_field_name = "next"

    def test_func(self):
        return self.request.user.is_staff

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied("Cette action est reservee a l'administrateur.")
        return super().handle_no_permission()


class ArticleListView(ListView):
    model = Article
    template_name = "blog/article_list.html"
    context_object_name = "articles"
    paginate_by = 6

    def get_queryset(self):
        queryset = Article.objects.select_related("auteur")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(
            statut=StatutPublication.PUBLIE,
            date_publication__lte=timezone.now(),
        )


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/article_detail.html"
    context_object_name = "article"

    def get_queryset(self):
        queryset = Article.objects.select_related("auteur")
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(
            statut=StatutPublication.PUBLIE,
            date_publication__lte=timezone.now(),
        )


class ArticleCreateView(StaffRequiredMixin, CreateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"

    def form_valid(self, form):
        form.instance.auteur = self.request.user
        response = super().form_valid(form)
        messages.success(self.request, "L'article a ete cree avec succes.")
        return response


class ArticleUpdateView(StaffRequiredMixin, UpdateView):
    model = Article
    form_class = ArticleForm
    template_name = "blog/article_form.html"

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "L'article a ete mis a jour.")
        return response


class ArticleDeleteView(StaffRequiredMixin, DeleteView):
    model = Article
    template_name = "blog/article_confirm_delete.html"
    success_url = reverse_lazy("blog:article_list")

    def form_valid(self, form):
        titre = self.object.titre
        response = super().form_valid(form)
        messages.success(self.request, f"L'article '{titre}' a ete supprime.")
        return response
