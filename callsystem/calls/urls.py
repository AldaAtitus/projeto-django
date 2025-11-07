from django.urls import path
from . import views

urlpatterns = [
    path('', views.call_list, name='call_list'),
    path('add/', views.add_call, name='add_call'),
    path('complete/<int:call_id>/', views.complete_call, name='complete_call'),
    path('delete/<int:call_id>/', views.delete_call, name='delete_call'),
]