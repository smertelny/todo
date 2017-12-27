from rest_framework import viewsets

from todo_list.models import TODO
from .serializers import TODOSerializer

class ToDoViewSet(viewsets.ModelViewSet):
    queryset = TODO.objects.all()
    serializer_class = TODOSerializer