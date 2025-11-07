from django.shortcuts import render, redirect, get_object_or_404
from .models import Call
import redis, json 

redis_client = redis.Redis(host='localhost', port=6379, db=0)

def call_list(request):
    calls = Call.objects.all()
    return render(request, "calls/call_list.html", {"calls": calls})

def add_call(request):
    if request.method == "POST":
        cliente = request.POST["cliente"]
        descricao = request.POST["descricao"]
        call = Call.objects.create(cliente=cliente, descricao=descricao)
        # Publica evento no Redis
        message = {
            "system": "callsystem",
            "action": "created",
            "id": call.id,
            "cliente": call.cliente,
            "descricao": call.descricao,
            "status": call.status,
        }
        redis_client.publish("calls_channel", json.dumps(message))

        return redirect("call_list")
    return render(request, "calls/add_call.html")

def complete_call(request, call_id):
    call = get_object_or_404(Call, id=call_id)
    call.status = "concluida"
    call.save()
    message = {
        "system": "callsystem",
        "action": "completed",
        "id": call.id,
        "cliente": call.cliente,
        "descricao": call.descricao,
        "status": call.status,
    }
    redis_client.publish("calls_channel", json.dumps(message))
    return redirect("call_list")

def delete_call(request, call_id):
    call = get_object_or_404(Call, id=call_id)
    message = {
        "system": "callsystem",
        "action": "deleted",
        "id": call.id,
        "cliente": call.cliente,
        "descricao": call.descricao,
        "status": call.status,
    }
    redis_client.publish("calls_channel", json.dumps(message))
    call.delete()
    return redirect("call_list")
