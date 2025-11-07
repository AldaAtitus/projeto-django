import redis
import json

# Conectar ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Inscrever no canal (mesmo nome usado nas views)
pubsub = redis_client.pubsub()
pubsub.subscribe("tasks")

print("📡 Aguardando mensagens no Redis...")

for message in pubsub.listen():
    if message['type'] == 'message':
        try:
            data = json.loads(message['data'])
        except Exception as e:
            print(f"Erro ao decodificar mensagem: {e}")
            continue

        # Identificar ação (created ou completed)
        action = data.get("action", "created")

        # Mostrar no terminal
        print(f"[{action.upper()}] Nova Task recebida: {data}")

        # Salvar em arquivo .txt
        with open("tasks_log.txt", "a", encoding="utf-8") as f:
            f.write(
                f"[{action.upper()}] ID: {data['id']} | "
                f"Título: {data['title']} | "
                f"Concluída: {data['completed']}\n"
            )
