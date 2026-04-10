from django.contrib.auth import views as auth_views
from django.urls import path

from .views import (
    ArticleCreateView,
    ArticleDeleteView,
    ArticleDetailView,
    ArticleListView,
    ArticleUpdateView,
)

app_name = "blog"

urlpatterns = [
    path("", ArticleListView.as_view(), name="article_list"),
    path("deconnexion/", auth_views.LogoutView.as_view(), name="logout"),
    path("article/<int:pk>/", ArticleDetailView.as_view(), name="article_detail"),
    path("article/nouveau/", ArticleCreateView.as_view(), name="article_create"),
    path(
        "article/<int:pk>/modifier/",
        ArticleUpdateView.as_view(),
        name="article_update",
    ),
    path(
        "article/<int:pk>/supprimer/",
        ArticleDeleteView.as_view(),
        name="article_delete",
    ),
]
