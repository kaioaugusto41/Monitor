from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse


# 6 - PÁGINA DE RELATÓRIOS
def relatorios(request):


    # 1.6 - INÍCIO DOS DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        'maquinas': Maquina.objects.all(),                                                          # 1.6.1 - Variável com comando que busca todas as máquinas cadastradas no banco.

        # 1.6.2 - INÍCIO DAS MÁQUINAS NA PÁGINA GERAL
        'maquina1': Maquina.objects.get(id=1),                                                      # 1.6.2.1 - Buscando o nome da máquina 1 no banco.
        'maquina2': Maquina.objects.get(id=2),                                                      # 1.6.2.2 - Buscando o nome da máquina 3 no banco.
        'maquina3': Maquina.objects.get(id=3),                                                      # 1.6.2.3 - Buscando o nome da máquina 4 no banco.
        'maquina4': Maquina.objects.get(id=4),                                                      # 1.6.2.4 - Buscando o nome da máquina 5 no banco.
        'maquina5': Maquina.objects.get(id=5),                                                      # 1.6.2.5 - Buscando o nome da máquina 6 no banco.
        'maquina6': Maquina.objects.get(id=6),                                                      # 1.6.2.6 - Buscando o nome da máquina 7 no banco.
        # @MQGERAL1#
        #'maquina5': Maquina.objects.get(id=id da máquina nova),                                    # 1.6.2.7 - Buscando o nome da máquina 5 no banco.
      
    }

    return render(request, 'relatorios.html', dados)