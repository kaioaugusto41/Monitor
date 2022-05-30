from django.shortcuts import render
from dash.models import Maquina, Paradas_tipos

def motivos_paradas(request):
    dados = {
        'motivos_paradas': Paradas_tipos.objects.all()
    }
    return render(request, 'motivos_paradas.html', dados)