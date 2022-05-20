from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('geral', views.geral, name='geral'),
    path('producao', views.producao, name='producao'),
    path('paradas', views.paradas, name='paradas'),
    path('<int:id_maquina>', views.maquina, name='maquina'),
    path('relatorios', views.relatorios, name='relatorios')
]
