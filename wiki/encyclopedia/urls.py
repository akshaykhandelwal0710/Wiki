from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name = "index"), 
    path("new_entry", views.new, name = "new"), 
    path("random_entry", views.rand, name = "random"), 
    path("wiki/<str:title>", views.index, name = "title"), 
    path("edit/<str:entry>", views.edit, name = "edit")
]
