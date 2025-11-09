from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def task_list(request):
    tasks = Task.objects.filter(parent__isnull=True)
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    all_tasks = Task.objects.all()
    if request.method == 'POST':
        title = request.POST['title']
        parent_id = request.POST.get('parent')
        parent = Task.objects.get(id=parent_id) if parent_id else None
        task = Task.objects.create(title=title, parent=parent)
        #Publica no Redis
        message = {
            "action": "created",
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }
        redis_client.publish("tasks", json.dumps(message))

        return redirect('task_list')
    return render(request, 'tasks/add_task.html', {'tasks': all_tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.completed = True
    task.save()

    message = {
        "action": "completed",
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
    }
    redis_client.publish("tasks", json.dumps(message))

    return redirect('task_list')

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)

    message = {
        "action": "deleted",
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
    }
    redis_client.publish("tasks", json.dumps(message))

    task.delete()
    return redirect('task_list')
