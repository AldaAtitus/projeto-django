import redis
import json

# Conectar ao Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

# Dados da task para publicar
task = {
    "id": 3,
    "title": "Task de teste via publisher",
    "completed": False
}

# Publicar no canal
redis_client.publish("tasks_channel", json.dumps(task))
print("✅ Mensagem publicada com sucesso!")