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
from .funcoes.consultas_banco import adicionaParadasListas_, consultaProducao, adicionaProducaoLista
from .funcoes.ordenaLista import ordenaLista

def index(request):

    # 1.1 - LISTA DE PARADAS POR MÁQUINA
    lista_paradas_maquina1 = []                                                                     # 1.1.1 - Contém todas as paradas da máquina 1
    lista_paradas_maquina3 = []                                                                     # 1.1.2 - Contém todas as paradas da máquina 3
    lista_paradas_maquina4 = []                                                                     # 1.1.4 - Contém todas as paradas da máquina 4
    lista_paradas_maquina5 = []                                                                     # 1.1.5 - Contém todas as paradas da máquina 5
    lista_paradas_maquina6 = []                                                                     # 1.1.6 - Contém todas as paradas da máquina 7
    lista_paradas_maquina7 = []                                                                     # 1.1.7 - Contém todas as paradas da máquina 7
    # @MQPARADAS1#
    # lista_paradas_maquina(id da máquina nova) = []                                                                   

    ordenaLista(lista_paradas_maquina1)
    ordenaLista(lista_paradas_maquina3)
    ordenaLista(lista_paradas_maquina4)
    ordenaLista(lista_paradas_maquina5)
    ordenaLista(lista_paradas_maquina6)
    ordenaLista(lista_paradas_maquina7)

    # 1.1 - REQUISIÇÃO DA EDIÇÃO DOS NOMES DAS MÁQUINAS 
    if request.method == 'GET':                                                                     # 1.1.1 - Se houver uma requisição do tipo GET na página...
        renomeiaMaquina(request, 'nome_maquina_antigo',  'nome_maquina_novo')
  

    # 1.2 - PRODUÇÃO DAS MÁQUINAS SEM FILTRO (PADRÃO)
    lista_producao_index = []                                                                       # 1.2.1 - Lista que contém todas as produções de todas as máquinas.
    data_antiga_index = str(datetime.now())[:11] + '00:00:01'                                       # 1.2.2 - Data antiga sem filtro.
    data_nova_index = str(datetime.now())[:19]                                                      # 1.2.3 - Data atual sem filtro.
    adicionaProducaoLista(data_antiga_index, data_nova_index, lista_producao_index)
    
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina1, 1)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina3, 3)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina4, 4)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina5, 5)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina6, 6)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina7, 7)

    maquinas_filtradas = []                                                                         # 1.2.9 - Lista de ids das máquinas a serem exibidas na página inicial (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 1.2.10 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 1.2.10.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)

    # 1.3 - PRODUÇÃO DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 1.3.1 - Se houver uma requisição do tipo POST na página...
        maquinas_filtradas = []                                                                     # 1.3.2 - Lista de máquinas com filtro...
        filtraMaquinas('POST', request, maquinas_filtradas)

        adicionaProducaoLista(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_producao_index)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina1, 1)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina3, 3)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina4, 4)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina5, 5)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina6, 6)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina7, 7)

    # 1.4 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        # MÁQUINAS QUE SERÃO MOSTRADAS SEM FILTRO (TODAS)
        'maquinas': Maquina.objects.all(),

        'paradas_tipos': Paradas_tipos.objects.all(),
        
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
        

        # 1.4.1 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'paradas_maquina1': len(lista_paradas_maquina1),                                            # 1.4.1.1 - Variável que conterá a quantidade de paradas da máquina 1.
        'paradas_maquina3': len(lista_paradas_maquina3),                                            # 1.4.1.2 - Variável que conterá a quantidade de paradas da máquina 3.
        'paradas_maquina4': len(lista_paradas_maquina4),                                            # 1.4.1.3 - Variável que conterá a quantidade de paradas da máquina 4.
        'paradas_maquina5': len(lista_paradas_maquina5),                                            # 1.4.1.4 - Variável que conterá a quantidade de paradas da máquina 5.
        'paradas_maquina6': len(lista_paradas_maquina6),                                            # 1.4.1.5 - Variável que conterá a quantidade de paradas da máquina 6.
        'paradas_maquina7': len(lista_paradas_maquina7),                                            # 1.4.1.6 - Variável que conterá a quantidade de paradas da máquina 7.
        # @MQPARADAS7#
        #'paradas_maquina(id)': len(lista_paradas_maquina5),

        # 1.4.2 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 1
        'parada_motivo1_maquina1': int(lista_paradas_maquina1.count(1)),                                 # 1.4.2.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 1.
        'parada_motivo2_maquina1': int(lista_paradas_maquina1.count(2)),                                 # 1.4.2.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 1.
        'parada_motivo3_maquina1': int(lista_paradas_maquina1.count(3)),                                 # 1.4.2.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 1.
        'parada_motivo4_maquina1': int(lista_paradas_maquina1.count(4)),                                 # 1.4.2.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 1.
        'parada_motivo5_maquina1': int(lista_paradas_maquina1.count(5)),                                 # 1.4.2.1 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 1.

        # 1.4.3 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 3
        'parada_motivo1_maquina3': lista_paradas_maquina3.count(1),                                 # 1.4.3.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 3.
        'parada_motivo2_maquina3': lista_paradas_maquina3.count(2),                                 # 1.4.3.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 3.
        'parada_motivo3_maquina3': lista_paradas_maquina3.count(3),                                 # 1.4.3.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 3.
        'parada_motivo4_maquina3': lista_paradas_maquina3.count(4),                                 # 1.4.3.1 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 3.
        'parada_motivo5_maquina3': lista_paradas_maquina3.count(5),                                 # 1.4.3.1 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 3.

        # 1.4.4 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 4
        'parada_motivo1_maquina4': lista_paradas_maquina4.count(1),                                 # 1.4.4.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 4.
        'parada_motivo2_maquina4': lista_paradas_maquina4.count(2),                                 # 1.4.4.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 4.
        'parada_motivo3_maquina4': lista_paradas_maquina4.count(3),                                 # 1.4.4.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 4.
        'parada_motivo4_maquina4': lista_paradas_maquina4.count(4),                                 # 1.4.4.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 4.
        'parada_motivo5_maquina4': lista_paradas_maquina4.count(5),                                 # 1.4.4.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 4.

        # 1.4.5 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 5
        'parada_motivo1_maquina5': lista_paradas_maquina5.count(1),                                 # 1.4.5.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 5.
        'parada_motivo2_maquina5': lista_paradas_maquina5.count(2),                                 # 1.4.5.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 5.
        'parada_motivo3_maquina5': lista_paradas_maquina5.count(3),                                 # 1.4.5.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 5.
        'parada_motivo4_maquina5': lista_paradas_maquina5.count(4),                                 # 1.4.5.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 5.
        'parada_motivo5_maquina5': lista_paradas_maquina5.count(5),                                 # 1.4.5.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 5.

        # 1.4.6 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 6
        'parada_motivo1_maquina6': lista_paradas_maquina6.count(1),                                 # 1.4.6.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 6.
        'parada_motivo2_maquina6': lista_paradas_maquina6.count(2),                                 # 1.4.6.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 6.
        'parada_motivo3_maquina6': lista_paradas_maquina6.count(3),                                 # 1.4.6.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 6.
        'parada_motivo4_maquina6': lista_paradas_maquina6.count(4),                                 # 1.4.6.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 6.
        'parada_motivo5_maquina6': lista_paradas_maquina6.count(5),                                 # 1.4.6.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 6.

        # 1.4.6 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 7
        'parada_motivo1_maquina7': lista_paradas_maquina7.count(1),                                 # 1.4.7.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 7.
        'parada_motivo2_maquina7': lista_paradas_maquina7.count(2),                                 # 1.4.7.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 7.
        'parada_motivo3_maquina7': lista_paradas_maquina7.count(3),                                 # 1.4.7.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 7.
        'parada_motivo4_maquina7': lista_paradas_maquina7.count(4),                                 # 1.4.7.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 7.
        'parada_motivo5_maquina7': lista_paradas_maquina7.count(5),                                 # 1.4.7.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 7.

        'ultima_atualizacao': datetime.now()                                                        # 1.4.9 - Função que pega a data e o horário atual para indicar a última atualização.
 
    }

    return render(request, 'index.html', dados)                                                     # 1.5 Função que renderiza a página index.html com os dados referenciados anteriormente.
