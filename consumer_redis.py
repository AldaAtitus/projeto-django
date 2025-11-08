import redis
import json
from datetime import datetime

# Conexão com Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Escuta os dois canais: CallSystem e TaskManager
pubsub = redis_client.pubsub()
pubsub.subscribe("calls_channel", "tasks")

print("📡 Escutando eventos do CallSystem e TaskManager...")

def ts():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

for message in pubsub.listen():
    if message['type'] != 'message':
        continue

    try:
        data = json.loads(message['data'])
    except Exception as e:
        print(f"Erro ao decodificar: {e}")
        continue

    channel = message['channel'].decode()
    action = data.get("action", "unknown").upper()

    # Eventos do CallSystem
    if channel == "calls_channel":
        cliente = data.get("cliente", "")
        descricao = data.get("descricao", "")
        status = data.get("status", "")
        if action == "CREATED":
            print(f"{ts()} [CALLSYSTEM] ➕ Nova chamada: Cliente={cliente} | Desc={descricao} | Status={status}")
        elif action == "COMPLETED":
            print(f"{ts()} [CALLSYSTEM] ✅ Chamada concluída: Cliente={cliente} | Desc={descricao} | Status={status}")
        elif action == "DELETED":
            print(f"{ts()} [CALLSYSTEM] ❌ Chamada removida: Cliente={cliente} | Desc={descricao} | Status={status}")
        with open("calls_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{ts()} [CALLSYSTEM-{action}] {data}\n")

    # Eventos do TaskManager
    elif channel == "tasks":
        title = data.get("title", "")
        completed = data.get("completed", False)
        if action == "CREATED":
            print(f"{ts()} [TASKMANAGER] ➕ Nova tarefa: Título={title} | Concluída={completed}")
        elif action == "COMPLETED":
            print(f"{ts()} [TASKMANAGER] ✅ Tarefa concluída: Título={title} | Concluída={completed}")
        elif action == "DELETED":
            print(f"{ts()} [TASKMANAGER] ❌ Tarefa removida: Título={title} | Concluída={completed}")
        with open("tasks_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{ts()} [TASKMANAGER-{action}] {data}\n")
