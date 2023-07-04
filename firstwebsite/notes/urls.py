from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("topic/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("note/<int:note_id>/", views.note_detail, name="note_detail"),
    path("topic/create/", views.topic_create, name="topic_create"),
    path("topic/edit/<int:topic_id>", views.topic_edit, name="topic_edit"),
    path("note/create/", views.note_create, name="note_create"),
    path("note/edit/<int:note_id>", views.note_edit, name="note_edit"),
    path("topic/delete/<int:topic_id>", views.topic_delete, name="topic_delete"),
    path("note/delete/<int:note_id>", views.note_delete, name="note_delete"),
]