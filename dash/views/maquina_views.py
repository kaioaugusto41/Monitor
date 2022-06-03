from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from dash.views.funcoes.consultas_banco import adicionaParadasLista, adicionaProducaoLista
from dash.views.funcoes.pega_datas import dataFinal, dataInicial


# 1 - PÁGINA DE CADA MÁQUINA (MENÚ)
def maquina(request, id_maquina):

    data_antiga_maquina = str(datetime.now())[:11] + '00:00:01'                                     # 1.2.1 - Data antiga sem filtro.
    data_nova_maquina = str(datetime.now()) [:19]                                                   # 1.2.2 - Data nova sem filtro.
    
    lista_producao_maquina = []
    adicionaProducaoLista(data_antiga_maquina, data_nova_maquina, lista_producao_maquina)

    lista_paradas_maquina = [] 
    adicionaParadasLista(data_antiga_maquina, data_nova_maquina, lista_paradas_maquina)
    
    # 1.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 1.5.1 - Se houver uma requisição do tipo POST na página...

        adicionaProducaoLista(dataInicial('POST', request, 'data_antiga_maquina', 'hora_antiga_maquina'), dataFinal('POST', request, 'data_nova_maquina', 'hora_nova_maquina'), lista_producao_maquina)
        adicionaParadasLista(dataInicial('POST', request, 'data_antiga_maquina', 'hora_antiga_maquina'), dataFinal('POST', request, 'data_nova_maquina', 'hora_nova_maquina'), lista_paradas_maquina)
    
    dados = {
        'maquina': get_object_or_404(Maquina, pk=id_maquina),
        'maquinas': Maquina.objects.all(),
        'motivos_paradas': Paradas_tipos.objects.all(),

        # 1.6.2 - INÍCIO DAS MÁQUINAS NA PÁGINA GERAL
        'maquina1': Maquina.objects.get(id=1),                                                      # 1.6.2.1 - Buscando o nome da máquina 1 no banco.
        'maquina2': Maquina.objects.get(id=2),                                                      # 1.6.2.2 - Buscando o nome da máquina 3 no banco.
        'maquina3': Maquina.objects.get(id=3),                                                      # 1.6.2.3 - Buscando o nome da máquina 4 no banco.
        'maquina4': Maquina.objects.get(id=4),                                                      # 1.6.2.4 - Buscando o nome da máquina 5 no banco.
        'maquina5': Maquina.objects.get(id=5),                                                      # 1.6.2.5 - Buscando o nome da máquina 6 no banco.
        'maquina6': Maquina.objects.get(id=6),                                                      # 1.6.2.6 - Buscando o nome da máquina 7 no banco.
        # @MQMAQUINA1#
        #'maquina5': Maquina.objects.get(id=id da máquina nova),                                    # 1.6.2.7 - Buscando o nome da máquina 5 no banco.

        # 1.6.3 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS
        'producao_maquina1': lista_producao_maquina.count(1),                                       # 1.6.3.1 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina2': lista_producao_maquina.count(2),                                       # 1.6.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina3': lista_producao_maquina.count(3),                                       # 1.6.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina4': lista_producao_maquina.count(4),                                       # 1.6.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina5': lista_producao_maquina.count(5),                                       # 1.6.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina6': lista_producao_maquina.count(6),                                       # 1.6.3.6 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7 
        # @MQMAQUINA2#
        #'producao_maquina5': lista_producao_maquina.count(id da máquina nova),                     # 1.6.3.7 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        
        # 1.6.4 - INÍCIO DADOS DE PARADAS DAS MÁQUINAS
        'paradas_maquina1': lista_paradas_maquina.count(1),                                         # 1.6.4.1 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 1
        'paradas_maquina2': lista_paradas_maquina.count(2),                                         # 1.6.4.2 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 3
        'paradas_maquina3': lista_paradas_maquina.count(3),                                         # 1.6.4.3 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 4
        'paradas_maquina4': lista_paradas_maquina.count(4),                                         # 1.6.4.4 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
        'paradas_maquina5': lista_paradas_maquina.count(5),                                         # 1.6.4.5 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 6
        'paradas_maquina6': lista_paradas_maquina.count(6),                                         # 1.6.4.6 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 7   
        #@MQMAQUINA3#
        #'paradas_maquina5': lista_paradas_maquina.count(id da máquina nova),                       # 1.6.4.7 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
    
        'ultima_atualizacao': datetime.now()                                                        # 1.6.4.8 - Variável que pega a data e hora do último refresh na página.  
    }

    return render(request, 'maquina.html', dados)
