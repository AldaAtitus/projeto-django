import redis
import json

# Conectar ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Inscrever no canal
pubsub = redis_client.pubsub()
pubsub.subscribe("tasks_channel")

print("📡 Aguardando mensagens no Redis...")

for message in pubsub.listen():
    if message['type'] == 'message':
        data = json.loads(message['data'])
        print(f"Nova Task recebida: {data}")

        # Salvar em arquivo .txt
        with open("tasks_log.txt", "a", encoding="utf-8") as f:
            f.write(f"ID: {data['id']} | Título: {data['title']} | Concluída: {data['completed']}\n")