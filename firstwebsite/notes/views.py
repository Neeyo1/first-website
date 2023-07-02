from django.shortcuts import render
from django.http import HttpResponse
from .models import Topic, Note, Comment

# Create your views here.

def index(request):
    latest_topics_list = Topic.objects.order_by("-updated_at")
    context = {"latest_topics_list": latest_topics_list}
    return render(request, "notes/index.html", context)