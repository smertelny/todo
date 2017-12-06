from django.shortcuts import render, get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

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
    return render(request, 'todo/create_edit_task.html', {'form': form})

def make_task_done(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(TODO, pk=pk)
        task.isDone = True
        task.save()
        messages.add_message(request, messages.SUCCESS, 'Well done')
        return HttpResponseRedirect(reverse('todo:index'))

def edit(request, pk):
    data = get_object_or_404(TODO, pk=pk)

    if request.method == "POST":
        form = CreateTaskForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('todo:index'))
    else:
        form = CreateTaskForm(instance=data)
    return render(request, 'todo/create_edit_task.html', {'form': form})
