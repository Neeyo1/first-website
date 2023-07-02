from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Topic, Note, Comment

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