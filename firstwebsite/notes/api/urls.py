from django.urls import path

from . import views

urlpatterns = [
    path("", views.get_routes, name="get_routes"),
    path("topics/", views.get_topics, name="get_topics"),
    path("topic/<int:topic_id>/", views.get_topic, name="get_topic"),
    path("notes/", views.get_notes, name="get_notes"),
    path("note/<int:note_id>/", views.get_note, name="get_note"),
    path("user/<int:user_id>/", views.get_user, name="get_user"),
]