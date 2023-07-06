from django.urls import path

from . import views

urlpatterns = [
    #main page
    path("", views.index, name="index"),
    #topic
    path("topic/<int:topic_id>/", views.topic_detail, name="topic_detail"),
    path("topic/create/", views.topic_create, name="topic_create"),
    path("topic/edit/<int:topic_id>", views.topic_edit, name="topic_edit"),
    path("topic/delete/<int:topic_id>", views.topic_delete, name="topic_delete"),
    #note
    path("note/<int:note_id>/", views.note_detail, name="note_detail"),
    path("note/create/", views.note_create, name="note_create"),
    path("note/edit/<int:note_id>", views.note_edit, name="note_edit"),
    path("note/delete/<int:note_id>", views.note_delete, name="note_delete"),
    #comment
    path("comment/<int:comment_id>/", views.comment_detail, name="comment_detail"),
    path("comment/create/", views.comment_create, name="comment_create"),
    path("comment/edit/<int:comment_id>/", views.comment_edit, name="comment_edit"),
    path("comment/delete/<int:comment_id>/", views.comment_delete, name="comment_delete"),
    #login
    path("login/", views.login_to_page, name="login_to_page"),
    #logout
    path("logout/", views.logout_from_page, name="logout_from_page"),
    #register
    path("register/", views.register_to_page, name="register_to_page"),
    #user
    path("user/<int:user_id>/", views.user_detail, name="user_detail"),
]