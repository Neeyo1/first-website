from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Topic, Note, Comment
from django.contrib.auth.models import User
from .forms import TopicForm, NoteForm, CommentForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm

# Create your views here.

def index(request):
    context = {}
    q_topic = request.GET.get('topic') or ''
    topics = Topic.objects.filter(name__icontains = q_topic)
    #latest_topics_list = Topic.objects.order_by("-updated_at")
    #context = {"latest_topics_list": latest_topics_list}
    context["topics"] = topics
    return render(request, "notes/index.html", context)

def topic_detail(request, topic_id):
    context = {}
    q_notes = request.GET.get('note') or ''
    topic = get_object_or_404(Topic, pk=topic_id)
    notes = topic.note_set.filter(name__icontains = q_notes)
    context["topic"] = topic
    context["notes"] = notes
    return render(request, "notes/topic_detail.html", context)

@login_required(login_url="/notes/login/")
def topic_create(request):
    context = {}
    if request.method == "POST":
        form = TopicForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect("/notes/")
    else:
        form = TopicForm()
    context["form"] = form
    return render(request, "notes/create_edit_form.html", {"form": form})

@login_required(login_url="/notes/login/")
def topic_edit(request, topic_id):
    context = {}
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user != topic.author:
        return HttpResponse("You are not author of this topic")

    form = TopicForm(instance=topic)
    if request.method == "POST":
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(f"/notes/topic/{instance.id}/")
    context["form"] = form
    return render(request, "notes/create_edit_form.html", context)

@login_required(login_url="/notes/login/")
def topic_delete(request, topic_id):
    context = {}
    topic = get_object_or_404(Topic, pk=topic_id)

    if request.user != topic.author:
        return HttpResponse("You are not author of this topic")

    notes_children = len(topic.note_set.all()) or "0"
    if request.method == "POST":
        topic.delete()
        return HttpResponseRedirect("/notes/")
    context["object_to_delete"] = topic
    context["notes_children"] = notes_children
    return render(request, "notes/delete_form.html", context)

def note_detail(request, note_id):
    context = {}
    note = get_object_or_404(Note, pk=note_id)
    comments = note.comment_set.all().order_by('-created_at')
    context["note"] = note
    context["comments"] = comments
    return render(request, "notes/note_detail.html", context)

@login_required(login_url="/notes/login/")
def note_create(request):
    context = {}
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(f"/notes/note/{instance.id}/")
    else:
        '''last_url = request.META.get('HTTP_REFERER')
        slashes_list = []
        i = 0
        for char_in_url in last_url:
            if char_in_url == '/':
                slashes_list.append(i)
            i += 1
        last_topic_id = last_url[slashes_list[-2]+1:slashes_list[-1]]'''
        topic = request.GET.get('topic') or ''
        if topic == '':
            return HttpResponseRedirect("/notes/")
        form = NoteForm(initial={'topic': topic})
    context["form"] = form
    return render(request, "notes/create_edit_form.html", context)

@login_required(login_url="/notes/login/")
def note_edit(request, note_id):
    context = {}
    note = get_object_or_404(Note, pk=note_id)

    if request.user != note.author:
        return HttpResponse("You are not author of this note")

    form = NoteForm(instance=note)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            instance = form.save()
            return HttpResponseRedirect(f"/notes/note/{instance.id}/")
    context["form"] = form
    return render(request, "notes/create_edit_form.html", context)

@login_required(login_url="/notes/login/")
def note_delete(request, note_id):
    context = {}
    note = get_object_or_404(Note, pk=note_id)

    if request.user != note.author:
        return HttpResponse("You are not author of this note")

    comments_children = len(note.comment_set.all()) or "0"
    if request.method == "POST":
        topic = note.topic.id
        note.delete()
        return HttpResponseRedirect(f"/notes/topic/{topic}/")
    context["object_to_delete"] = note
    context["comments_children"] = comments_children
    return render(request, "notes/delete_form.html", context)

def comment_detail(request, comment_id):
    context = {}
    comment = get_object_or_404(Comment, pk=comment_id)
    context["comment"] = comment
    return render(request, "notes/comment_detail.html", context)

@login_required(login_url="/notes/login/")
def note_complete(request, note_id):
    context = {}
    note = get_object_or_404(Note, pk=note_id)

    if request.user != note.author:
        return HttpResponse("You are not author of this note")
    
    if request.method == "POST":
        note.completed = not note.completed
        note.save()
        return HttpResponseRedirect(f"/notes/note/{note.id}")

    context["object_to_complete"] = note
    return render(request, "notes/complete_form.html", context)

def comment_detail(request, comment_id):
    context = {}
    comment = get_object_or_404(Comment, pk=comment_id)
    context["comment"] = comment
    return render(request, "notes/comment_detail.html", context)

@login_required(login_url="/notes/login/")
def comment_create(request):
    context = {}
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['note'].is_completed():
                return HttpResponse("You cannot add comment in completed note")
            instance = form.save(commit=False)
            instance.author = request.user
            instance.save()
            return HttpResponseRedirect(f"/notes/note/{instance.note.id}/")
    else:
        '''last_url = request.META.get('HTTP_REFERER')
        slashes_list = []
        i = 0
        for char_in_url in last_url:
            if char_in_url == '/':
                slashes_list.append(i)
            i += 1
        last_notec_id = last_url[slashes_list[-2]+1:slashes_list[-1]]
        form = CommentForm(initial={'note': last_notec_id})'''
        note = request.GET.get('note') or ''
        if note == '':
            return HttpResponseRedirect("/notes/")
        form = CommentForm(initial={'note': note})
    context["form"] = form
    return render(request, "notes/create_edit_form.html", context)

@login_required(login_url="/notes/login/")
def comment_edit(request, comment_id):
    context = {}
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return HttpResponse("You are not author of this comment")

    form = CommentForm(instance=comment)
    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(f"/notes/note/{comment.note.id}/")
    context["form"] = form
    return render(request, "notes/create_edit_form.html", context)

@login_required(login_url="/notes/login/")
def comment_delete(request, comment_id):
    context = {}
    comment = get_object_or_404(Comment, pk=comment_id)

    if request.user != comment.author:
        return HttpResponse("You are not author of this comment")

    if request.method == "POST":
        comment.delete()
        return HttpResponseRedirect(f"/notes/note/{comment.note.id}/")
    context["object_to_delete"] = comment
    return render(request, "notes/delete_form.html", context)

def login_to_page(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            print("Success")
            next_url = request.GET.get('next') or "/notes/"
            return HttpResponseRedirect(next_url)
        else:
            error_message = "Incorrect login or password"
            context["error_message"] = error_message
            return render(request, "notes/login_form.html", context)
    return render(request, "notes/login_form.html", context)

def logout_from_page(request):
    logout(request)
    return HttpResponseRedirect("/notes/")

def register_to_page(request):
    context = {}
    form = UserCreationForm()
    context["form"] = form
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponseRedirect("/notes/")
        else:
            error_message = "Error during registration"
            context["error_message"] = error_message
            context["form"] = form
            return render(request, "notes/register_form.html", context)
    return render(request, "notes/register_form.html", context)

def user_detail(request, user_id):
    context = {}
    user = get_object_or_404(User, pk=user_id)
    topics = user.topic_set.all().order_by('-created_at')
    notes = user.note_set.all().order_by('-created_at')
    context['topics'] = topics
    context['user'] = user
    context['notes'] = notes
    return render(request, "notes/user_detail.html", context)
