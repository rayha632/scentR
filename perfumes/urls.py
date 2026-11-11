from django.urls import path

from . import views

urlpatterns = [
    path("", views.search_perfumes, name="home"),
    path("search/", views.search_perfumes, name="perfume-search"),
    path("perfumes/<str:perfume_id>/", views.perfume_detail, name="perfume-detail"),
]
