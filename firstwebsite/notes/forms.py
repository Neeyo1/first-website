from django import forms
from .models import Topic, Note, Comment

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name', 'description']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'name', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['note', 'message']