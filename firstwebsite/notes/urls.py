from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("topic/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("note/<int:note_id>/", views.note_detail, name="note_detail"),
]