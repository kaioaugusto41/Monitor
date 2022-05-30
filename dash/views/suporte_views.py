from django.shortcuts import render
from dash.models import Maquina, Paradas_tipos

def suporte(request):
    return render(request, 'suporte.html')