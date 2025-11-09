from django.contrib import admin
from .models import Task

class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "completed")   # colunas visíveis
    list_filter = ("completed",)                  # filtros laterais
    search_fields = ("title",)                    # barra de busca

admin.site.register(Task, TaskAdmin)
