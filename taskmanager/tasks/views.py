from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
import redis
import json

# Conexão com Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

def task_list(request):
    tasks = Task.objects.all()
    return render(request, 'tasks/task_list.html', {'tasks': tasks})

def add_task(request):
    if request.method == 'POST':
        title = request.POST['title']
        task = Task.objects.create(title=title)

        # Publicar no Redis quando criada
        message = {
            "action": "created",
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }
        redis_client.publish("tasks", json.dumps(message))

        return redirect('task_list')
    return render(request, 'tasks/add_task.html')

def complete_task(request, task_id):
    task = Task.objects.get(id=task_id)
    task.completed = True
    task.save()

    # Publicar no Redis quando concluída
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
    task.delete()

    # Publicar no Redis quando removida
    message = {
        "action": "deleted",
        "id": task_id,
        "title": task.title,
        "completed": task.completed,
    }
    redis_client.publish("tasks", json.dumps(message))

    return redirect('task_list')