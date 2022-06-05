from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from dash.views.funcoes.consultas_banco import adicionaParadasLista, adicionaProducaoLista
from .funcoes.pega_datas import dataInicial, dataFinal


# 1 - PÁGINA GERAL (MENÚ)
def geral(request):

    data_antiga_geral = str(datetime.now())[:11] + '00:00:01'                                      # 1.2.1 - Data antiga sem filtro.
    data_nova_geral = str(datetime.now())[:19]

    # DADOS PARA JOGAR E BAIXAR RELATÓRIO NA VIEWS PDF
    data_antiga_relatorio = str(datetime.now())[:11]
    hora_antiga_relatorio = '00:00:01'
    data_nova_relatorio = str(datetime.now())[:11]
    hora_nova_relatorio = str(datetime.now())[11:19]

    lista_producao_geral = []                                                    # 1.2.2 - Data nova sem filtro.
    adicionaProducaoLista(data_antiga_geral, data_nova_geral, lista_producao_geral)                                                          # 1.3.4.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    lista_paradas_geral = []
    adicionaParadasLista(data_antiga_geral, data_nova_geral, lista_paradas_geral) 
    
    # 1.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':
        data_antiga_relatorio = request.POST.get('data_antiga_geral', False)
        hora_antiga_relatorio = request.POST.get('hora_antiga', False)
        data_nova_relatorio = request.POST.get('data_nova_geral', False)                                                                     # 1.5.1 - Se houver uma requisição do tipo POST na página... 
        hora_nova_relatorio = request.POST.get('hora_nova', False)
        
        adicionaProducaoLista(dataInicial('POST', request, 'data_antiga_geral', 'hora_antiga'), dataFinal('POST', request, 'data_nova_geral', 'hora_nova'), lista_producao_geral)
        adicionaParadasLista(dataInicial('POST', request, 'data_antiga_geral', 'hora_antiga'), dataFinal('POST', request, 'data_nova_geral', 'hora_nova'), lista_paradas_geral)

    

    # 1.6 - INÍCIO DOS DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        'data_antiga_relatorio': data_antiga_relatorio,
        'hora_antiga_relatorio': hora_antiga_relatorio,
        'data_nova_relatorio': data_nova_relatorio,
        'hora_nova_relatorio': hora_nova_relatorio,


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

        # 1.6.3 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS
        'producao_maquina1': lista_producao_geral.count(1),                                        # 1.6.3.1 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina2': lista_producao_geral.count(2),                                        # 1.6.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina3': lista_producao_geral.count(3),                                        # 1.6.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina4': lista_producao_geral.count(4),                                        # 1.6.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina5': lista_producao_geral.count(5),                                        # 1.6.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina6': lista_producao_geral.count(6),                                        # 1.6.3.6 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7 
        # @MQGERAL2#
        #'producao_maquina5': lista_producao_geral.count(id da máquina nova),                      # 1.6.3.7 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        
        # 1.6.4 - INÍCIO DADOS DE PARADAS DAS MÁQUINAS
        'paradas_maquina1': lista_paradas_geral.count(1),                                          # 1.6.4.1 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 1
        'paradas_maquina2': lista_paradas_geral.count(2),                                          # 1.6.4.2 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 3
        'paradas_maquina3': lista_paradas_geral.count(3),                                          # 1.6.4.3 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 4
        'paradas_maquina4': lista_paradas_geral.count(4),                                          # 1.6.4.4 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
        'paradas_maquina5': lista_paradas_geral.count(5),                                          # 1.6.4.5 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 6
        'paradas_maquina6': lista_paradas_geral.count(6),                                          # 1.6.4.6 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 7   
        #@MQGERAL3#
        #'paradas_maquina5': lista_paradas_geral.count(id da máquina nova),                        # 1.6.4.7 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
        
        'ultima_atualizacao': datetime.now()                                                         # 1.6.4.8 - Variável que pega a data e hora do último refresh na página.
    }

    return render(request, 'geral.html', dados)                                                      # 3 - Função que renderiza a página geral.html com os dados referenciados anteriormente.
