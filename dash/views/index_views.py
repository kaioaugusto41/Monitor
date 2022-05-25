from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from dash.views.funcoes.filtra_maquinas import filtraMaquinas
from dash.views.funcoes.pega_datas import dataFinal, dataInicial
from .funcoes.renomeia_maquinas import renomeiaMaquina
from .funcoes.consultas_banco import consultaProducao, adicionaProducaoLista

def index(request):

    # 1.1 - REQUISIÇÃO DA EDIÇÃO DOS NOMES DAS MÁQUINAS 
    if request.method == 'GET':                                                                     # 1.1.1 - Se houver uma requisição do tipo GET na página...
        renomeiaMaquina(request, 'nome_maquina_antigo',  'nome_maquina_novo')
  

    # 1.2 - PRODUÇÃO DAS MÁQUINAS SEM FILTRO (PADRÃO)
    lista_producao_index = []                                                                       # 1.2.1 - Lista que contém todas as produções de todas as máquinas.
    data_antiga_index = str(datetime.now())[:11] + '00:00:01'                                       # 1.2.2 - Data antiga sem filtro.
    data_nova_index = str(datetime.now())[:19]                                                      # 1.2.3 - Data atual sem filtro.
    adicionaProducaoLista(data_antiga_index, data_nova_index, lista_producao_index)
    
    maquinas_filtradas = []                                                                         # 1.2.9 - Lista de ids das máquinas a serem exibidas na página inicial (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 1.2.10 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 1.2.10.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)

    # 1.3 - PRODUÇÃO DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 1.3.1 - Se houver uma requisição do tipo POST na página...
        maquinas_filtradas = []                                                                     # 1.3.2 - Lista de máquinas com filtro...
        filtraMaquinas('POST', request, maquinas_filtradas)

        adicionaProducaoLista(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_producao_index)

    # 1.4 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        # MÁQUINAS QUE SERÃO MOSTRADAS SEM FILTRO (TODAS)
        'maquinas': Maquina.objects.all(),
        
        # MÁQUINAS QUE SERÃO MOSTRADAS COM FILTRO (AS QUE O USUÁRIO SELECIONAR APENAS)
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),                    # 1.4.1 - Comando que busca todas as máquinas cadastradas no banco.

        #INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA INDEX
        'producao_maquina1': lista_producao_index.count(1),                                         # 1.4.2 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_index.count(3),                                         # 1.4.3 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_index.count(4),                                         # 1.4.4 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_index.count(5),                                         # 1.4.5 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina6': lista_producao_index.count(6),                                         # 1.4.6 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina7': lista_producao_index.count(7),                                         # 1.4.7 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 7      
        # @PMINDEX2#
        #'producao_maquina8': lista_producao_index.count(id da máquina nova),                       # 1.4.8 - Conta quantas peças foram produzidas no período filtrado na máquina com o ID 8
        
        'ultima_atualizacao': datetime.now()                                                        # 1.4.9 - Função que pega a data e o horário atual para indicar a última atualização.
 
    }

    return render(request, 'index.html', dados)                                                     # 1.5 Função que renderiza a página index.html com os dados referenciados anteriormente.
