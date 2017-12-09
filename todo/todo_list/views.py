from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

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

@csrf_exempt
@require_POST
def make_task_done(request, pk):
    if request.method == 'POST':
        task = get_object_or_404(TODO, pk=pk)
        if task.isDone:
            messages.add_message(request, messages.WARNING, 'The Task is already done')
        else:
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
