from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST

from .models import TODO
from .forms import CreateTaskForm

def index(request):
    data = TODO.objects.filter(isDone=False)
    return render(request, "todo/index.html", {"data":data})

def new_task(request):
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('todo:index'))
    else:
        form = CreateTaskForm()
    return render(request, 'todo/create_edit_task.html', {'form': form, 'active': 'new task'})

def edit(request, pk):
    data = get_object_or_404(TODO, pk=pk)
    if data.isDone:
        messages.add_message(request, messages.WARNING, "Done task can't be edited")
        return HttpResponseRedirect(reverse('todo:index'))

    if request.method == "POST":
        form = CreateTaskForm(request.POST, instance=data)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('todo:index'))
    else:
        form = CreateTaskForm(instance=data)
    return render(request, 'todo/create_edit_task.html', {'form': form})

@require_POST
def make_task_done(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(TODO, pk=pk)
        if task.isDone:
            messages.add_message(request, messages.WARNING, 'The Task is already done.')
        else:
            task.isDone = True
            task.save()
            messages.add_message(request, messages.SUCCESS, 'Task is now done.')
        return HttpResponseRedirect(reverse('todo:index'))

def done_tasks_list(request):
    data = TODO.objects.filter(isDone=True).order_by('-pk')
    return render(request, "todo/done-list.html", {"data": data, 'active': 'done tasks'})

@require_POST
def make_task_in_progress(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(TODO, pk=pk)
        if not task.isDone:
            messages.add_message(request, messages.WARNING, 'The Task is not done yet.')
        else:
            task.isDone = False
            task.save()
            messages.add_message(request, messages.SUCCESS, 'The task is In Progress again.')
        return HttpResponseRedirect(reverse('todo:index'))
