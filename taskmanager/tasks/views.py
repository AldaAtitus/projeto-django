from django.shortcuts import render, redirect, get_object_or_404
from .models import Task
import redis, json

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def task_list(request):
    tasks = Task.objects.filter(parent__isnull=True)  # só tarefas principais
    return render(request, "tasks/task_list.html", {"tasks": tasks})

def add_task(request):
    if request.method == "POST":
        title = request.POST["title"]
        parent_id = request.POST.get("parent")
        parent = Task.objects.get(id=parent_id) if parent_id else None
        task = Task.objects.create(title=title, parent=parent)

        # Publica evento no Redis
        message = {
            "system": "taskmanager",
            "action": "created",
            "id": task.id,
            "title": task.title,
            "completed": task.completed,
        }
        redis_client.publish("tasks", json.dumps(message))
        return redirect("task_list")

    # Aqui está o detalhe: enviar todas as tarefas para o template
    tasks = Task.objects.all()
    return render(request, "tasks/add_task.html", {"tasks": tasks})

def complete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    # Completar tarefa e todas as subtarefas recursivamente
    def conclude_recursively(t):
        t.completed = True
        t.save()
        message = {
            "system": "taskmanager",
            "action": "completed",
            "id": t.id,
            "title": t.title,
            "completed": t.completed,
        }
        redis_client.publish("tasks", json.dumps(message))
        for sub in t.subtasks.all():
            conclude_recursively(sub)
# Chamar a função recursiva na tarefa principal
    conclude_recursively(task)
    return redirect("task_list")

def delete_task(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    message = {
        "system": "taskmanager",
        "action": "deleted",
        "id": task.id,
        "title": task.title,
        "completed": task.completed,
    }
    redis_client.publish("tasks", json.dumps(message))
    task.delete()
    return redirect("task_list")
