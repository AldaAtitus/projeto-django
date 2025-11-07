import redis
import json
from datetime import datetime

# Conectar ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Inscrever no canal de eventos
pubsub = redis_client.pubsub()
pubsub.subscribe("calls_channel")   # canal exclusivo para CallSystem

print("📡 Escutando eventos do CallSystem...")

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

    action = data.get("action", "unknown").upper()
    cliente = data.get("cliente", "")
    descricao = data.get("descricao", "")
    status = data.get("status", "")

    # Exibir no terminal
    print(f"{ts()} [CALLSYSTEM-{action}] Cliente: {cliente} | Desc: {descricao} | Status: {status}")

    # Registrar em arquivo
    with open("calls_log.txt", "a", encoding="utf-8") as f:
        f.write(f"{ts()} [CALLSYSTEM-{action}] {data}\n")
