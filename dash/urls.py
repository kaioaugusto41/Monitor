from django.urls import path
from dash.views import (
    gera_pdf_geral_views,
    index_views, 
    geral_views, 
    producao_views,
    paradas_views, 
    maquina_views, 
    relatorios_views,
 )
import dash

urlpatterns = [
    path('', index_views.index, name='index'),
    path('geral', geral_views.geral, name='geral'),
    path('producao', producao_views.producao, name='producao'),
    path('paradas', paradas_views.paradas, name='paradas'),
    path('<int:id_maquina>', maquina_views.maquina, name='maquina'),
    path('relatorios', relatorios_views.relatorios, name='relatorios'),
    path('gera_pdf_geral', gera_pdf_geral_views.gera_pdf_geral, name='gera_pdf_geral')
]
