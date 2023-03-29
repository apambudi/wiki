from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.show_entry, name="show_entry"),
    path("search", views.search, name="search"),
    path("new_page", views.new_page, name="new_page"),
    path("edit_page", views.edit_page, name="edit_page"),
    path("edit/<str:title>", views.edit_content, name="edit_content"),
    path("random_page", views.random_page, name="random_page"),
]