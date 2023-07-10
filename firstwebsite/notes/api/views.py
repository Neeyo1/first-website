from rest_framework.decorators import api_view
from rest_framework.response import Response
from notes.models import Topic, Note, User
from .serializers import TopicSerializer, NoteSerializer, UserSerializer

# Create your views here.

@api_view(['GET'])
def get_routes(request):
    routes = [
        'GET /api/topics',
        'GET /api/topic/:id',
        'GET /api/notes',
        'GET /api/note/:id',
        'GET /api/user/:id'
    ]
    return Response(routes)

@api_view(['GET'])
def get_topics(request):
    topics = Topic.objects.all()
    serializer = TopicSerializer(topics, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_topic(request, topic_id):
    topic = Topic.objects.get(id=topic_id)
    serializer = TopicSerializer(topic, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_notes(request):
    notes = Note.objects.all()
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def get_note(request, note_id):
    note = Note.objects.get(id=note_id)
    serializer = NoteSerializer(note, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def get_user(request, user_id):
    user = User.objects.get(id=user_id)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)