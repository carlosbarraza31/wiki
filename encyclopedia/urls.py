from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("searchResults", views.searchResults, name = "searchResults"),
    path("newPage", views.newPage, name = "newPage"),
    path("wiki/<str:title>/editPage", views.editPage, name = "editPage"),
    path("randomPage", views.randomPage, name = "randomPage"),
    path("wiki/<str:title>", views.entry, name = "entry")
]
