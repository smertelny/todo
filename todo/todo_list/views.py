from django.shortcuts import render, get_list_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import TODO
from .forms import CreateTaskForm

def index(request):
    data = TODO.objects.filter(isDone=False).order_by('-pk')
    return render(request, "todo/index.html", {"data":data})

def new_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
        return HttpResponseRedirect(reverse('todo:index'))
    else:
        form = CreateTaskForm()
    return render(request, 'todo/create_task.html', {'form': form})