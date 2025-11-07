from django.db import models

class Call(models.Model):
    cliente = models.CharField(max_length=100)
    descricao = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=[("pendente", "Pendente"), ("concluida", "Concluída")],
        default="pendente"
    )

    def __str__(self):
        return f"{self.cliente} - {self.status}"
