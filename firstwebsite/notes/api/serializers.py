from rest_framework.serializers import ModelSerializer
from notes.models import Topic, Note, User

class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = '__all__'

class NoteSerializer(ModelSerializer):
    class Meta:
        model = Note
        fields = '__all__'

class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'