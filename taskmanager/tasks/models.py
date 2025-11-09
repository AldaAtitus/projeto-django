from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import redis
import json

# Configura conexão com Redis
redis_client = redis.Redis(host='localhost', port=6379, db=0)

class Task(models.Model):
    title = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subtasks'
    )
    def __str__(self):
        return self.title

# Signal: dispara após salvar uma Task
@receiver(post_save, sender=Task)
def publish_task_to_redis(sender, instance, created, **kwargs):
    if created:  # só quando for nova
        message = {
            "id": instance.id,
            "title": instance.title,
            "completed": instance.completed,
        }
        redis_client.publish("tasks_channel", json.dumps(message))