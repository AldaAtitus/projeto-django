from django.contrib import admin
from .models import Call

class CallAdmin(admin.ModelAdmin):
    list_display = ("id", "cliente", "descricao", "status")
    list_filter = ("status",)
    search_fields = ("cliente", "descricao")

admin.site.register(Call, CallAdmin)
