from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Note, Comment
from .forms import TopicForm, NoteForm

# Create your views here.

def index(request):
    latest_topics_list = Topic.objects.order_by("-updated_at")
    context = {"latest_topics_list": latest_topics_list}
    return render(request, "notes/index.html", context)

def topic_detail(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    notes = topic.note_set.all()
    return render(request, "notes/topic_detail.html", {"topic": topic, "notes": notes})

def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    return render(request, "notes/note_detail.html", {"note": note})

def topic_create(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    else:
        form = TopicForm()
    return render(request, "notes/topic_create_edit_form.html", {"form": form})

def topic_edit(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)
    form = TopicForm(instance=topic)
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    context = {"form": form}
    return render(request, "notes/topic_create_edit_form.html", context)

def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    else:
        form = NoteForm()
    return render(request, "notes/topic_create_edit_form.html", {"form": form})

def note_edit(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    form = NoteForm(instance=note)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    context = {"form": form}
    return render(request, "notes/topic_create_edit_form.html", context)