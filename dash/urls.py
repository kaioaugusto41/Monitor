from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('geral', views.geral, name='geral'),
    path('producao', views.producao, name='producao'),
]
