from django.shortcuts import render, get_list_or_404

from .models import TODO

def index(request):
    data = TODO.objects.filter(isDone=False) #get_list_or_404(TODO)
    return render(request, "todo/index.html", {"data":data})
