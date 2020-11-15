from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),

    path("wiki/add", views.add, name="add"),
    path("wiki/random", views.random, name="random"),
    path("wiki/<str:title>", views.entry, name="entry"),
    path("wiki/edit/<str:title>", views.edit, name="edit"),
]
