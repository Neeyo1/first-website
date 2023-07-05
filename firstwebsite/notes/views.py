from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Note, Comment
from django.contrib.auth.models import User
from .forms import TopicForm, NoteForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    q_topic = request.GET.get('topic') or ''
    topics = Topic.objects.filter(name__icontains = q_topic)
    #latest_topics_list = Topic.objects.order_by("-updated_at")
    #context = {"latest_topics_list": latest_topics_list}
    context = {"topics": topics}
    return render(request, "notes/index.html", context)

def topic_detail(request, topic_id):
    q_notes = request.GET.get('note') or ''
    topic = get_object_or_404(Topic, pk=topic_id)
    notes = topic.note_set.filter(name__icontains = q_notes)
    return render(request, "notes/topic_detail.html", {"topic": topic, "notes": notes})

@login_required()
def topic_create(request):
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    else:
        form = TopicForm()
    return render(request, "notes/create_edit_form.html", {"form": form})

@login_required()
def topic_edit(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user != topic.author:
        return HttpResponse("You are not author of this topic")

    form = TopicForm(instance=topic)
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    context = {"form": form}
    return render(request, "notes/create_edit_form.html", context)

@login_required()
def topic_delete(request, topic_id):
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user != topic.author:
        return HttpResponse("You are not author of this topic")

    notes_children = len(topic.note_set.all()) or "0"
    if request.method == "POST":
        topic.delete()
        return HttpResponseRedirect("/notes/")
    context = {
        'object_to_delete': topic,
        'notes_children': notes_children
        }
    return render(request, "notes/delete_form.html", context)

def note_detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id)
    comments = note.comment_set.all()
    return render(request, "notes/note_detail.html", {"note": note, 'comments': comments})

@login_required()
def note_create(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    else:
        last_url = request.META.get('HTTP_REFERER')
        slashes_list = []
        i = 0
        for char_in_url in last_url:
            if char_in_url == '/':
                slashes_list.append(i)
            i += 1
        last_topic_id = last_url[slashes_list[-2]+1:slashes_list[-1]]
        form = NoteForm(initial={'topic': last_topic_id})
    return render(request, "notes/create_edit_form.html", {"form": form})

@login_required()
def note_edit(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if request.user != note.author:
        return HttpResponse("You are not author of this note")

    form = NoteForm(instance=note)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    context = {"form": form}
    return render(request, "notes/create_edit_form.html", context)

@login_required()
def note_delete(request, note_id):
    note = get_object_or_404(Note, pk=note_id)

    if request.user != note.author:
        return HttpResponse("You are not author of this note")

    comments_children = len(note.comment_set.all()) or "0"
    if request.method == "POST":
        note.delete()
        return HttpResponseRedirect("/notes/")
    context = {
        'object_to_delete': note,
        'comments_children': comments_children
        }
    return render(request, "notes/delete_form.html", context)

def comment_detail(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    return render(request, "notes/comment_detail.html", {"comment": comment})

@login_required()
def comment_create(request):
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    else:
        last_url = request.META.get('HTTP_REFERER')
        slashes_list = []
        i = 0
        for char_in_url in last_url:
            if char_in_url == '/':
                slashes_list.append(i)
            i += 1
        last_notec_id = last_url[slashes_list[-2]+1:slashes_list[-1]]
        form = CommentForm(initial={'note': last_notec_id})
    return render(request, "notes/create_edit_form.html", {"form": form})

@login_required()
def comment_edit(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return HttpResponse("You are not author of this comment")

    form = CommentForm(instance=comment)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect("/notes/")
    context = {"form": form}
    return render(request, "notes/create_edit_form.html", context)

@login_required()
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return HttpResponse("You are not author of this comment")

    if request.method == "POST":
        comment.delete()
        return HttpResponseRedirect("/notes/")
    context = {
        'object_to_delete': comment
        }
    return render(request, "notes/delete_form.html", context)

def login_to_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Success")
            return HttpResponseRedirect("/notes/")
        else:
            error_message = "Incorrct login or password"
            context = {'error_message': error_message}
            return render(request, "notes/login_register_form.html", context)
        
    context = {}
    return render(request, "notes/login_register_form.html", context)

def logout_from_page(request):
    logout(request)
    return HttpResponseRedirect("/notes/")