from django.urls import path
from . import views

urlpatterns = [
    path("", views.call_list, name="call_list"),  # rota raiz do app
    path("add/", views.add_call, name="add_call"),
    path("<int:call_id>/complete/", views.complete_call, name="complete_call"),
    path("<int:call_id>/delete/", views.delete_call, name="delete_call"),
]
