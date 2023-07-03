from django import forms
from .models import Topic, Note

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['author', 'name', 'description']

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['topic', 'author', 'name', 'description']