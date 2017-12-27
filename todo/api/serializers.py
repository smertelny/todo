
from rest_framework import serializers

from todo_list.models import TODO

class TODOSerializer(serializers.ModelSerializer):
    class Meta:
        model = TODO
        fields = ('id', 'header', 'description', 'isDone')