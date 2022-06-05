from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from dash.views.funcoes.consultas_banco import adicionaParadasListas_
from dash.views.funcoes.filtra_maquinas import filtraMaquinas
from .funcoes.pega_datas import dataInicial, dataFinal
from dash.views.funcoes.ordenaLista import ordenaLista


# 1 - PÁGINA PARADAS (MENÚ)
def paradas(request):

    # 1.1 - LISTA DE PARADAS POR MÁQUINA
    lista_paradas_maquina1 = []                                                                     # 1.1.1 - Contém todas as paradas da máquina 1
    lista_paradas_maquina2 = []                                                                     # 1.1.2 - Contém todas as paradas da máquina 3
    lista_paradas_maquina3 = []                                                                     # 1.1.4 - Contém todas as paradas da máquina 4
    lista_paradas_maquina4 = []                                                                     # 1.1.5 - Contém todas as paradas da máquina 5
    lista_paradas_maquina5 = []                                                                     # 1.1.6 - Contém todas as paradas da máquina 7
    lista_paradas_maquina6 = []                                                                     # 1.1.7 - Contém todas as paradas da máquina 7
    # @MQPARADAS1#
    # lista_paradas_maquina(id da máquina nova) = []                                                                   

    ordenaLista(lista_paradas_maquina1)
    ordenaLista(lista_paradas_maquina2)
    ordenaLista(lista_paradas_maquina3)
    ordenaLista(lista_paradas_maquina4)
    ordenaLista(lista_paradas_maquina5)
    ordenaLista(lista_paradas_maquina6)

    # 1.2 - PARADAS DAS MÁQUINAS SEM FILTRO
    lista_paradas = []                                                                              # 1.2.1 - Lista com todas as paradas de todas as máquinas.
    data_antiga_paradas = str(datetime.now())[:11] + '00:00:01'                                     # 1.2.2 - Data antiga sem filtro.
    data_nova_paradas = str(datetime.now()) [:19]                                                   # 1.2.3 - Data nova sem filtro.
    
    adicionaParadasListas_(data_antiga_paradas, data_nova_paradas, lista_paradas_maquina1, 1)
    adicionaParadasListas_(data_antiga_paradas, data_nova_paradas, lista_paradas_maquina2, 2)
    adicionaParadasListas_(data_antiga_paradas, data_nova_paradas, lista_paradas_maquina3, 3)
    adicionaParadasListas_(data_antiga_paradas, data_nova_paradas, lista_paradas_maquina4, 4)
    adicionaParadasListas_(data_antiga_paradas, data_nova_paradas, lista_paradas_maquina5, 5)
    adicionaParadasListas_(data_antiga_paradas, data_nova_paradas, lista_paradas_maquina6, 6)

    maquinas_filtradas = []                                                                         # 1.2.15 - Lista de ids das máquinas a serem exibidas na página Paradas (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 1.2.16 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 1.2.16.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)
    
    data_antiga_relatorio = str(datetime.now())[:11]
    hora_antiga_relatorio = '00:00:01'
    data_nova_relatorio = str(datetime.now())[:11]
    hora_nova_relatorio = str(datetime.now())[11:19]
    
    # 1.3 - PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 1.3.1 - Se houver uma requisição do tipo POST na página...
        data_antiga_relatorio = request.POST.get('data_antiga_paradas', False)
        hora_antiga_relatorio = request.POST.get('hora_antiga', False)
        data_nova_relatorio = request.POST.get('data_nova_paradas', False)
        hora_nova_relatorio = request.POST.get('hora_nova', False)
       
        maquinas_filtradas = []                                                                     # 1.3.2 - Lista de máquinas com filtro...
        filtraMaquinas('POST', request, maquinas_filtradas)                                      # 1.3.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)

        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_paradas', 'hora_antiga'), dataFinal('POST', request, 'data_nova_paradas', 'hora_nova'), lista_paradas_maquina1, 1)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_paradas', 'hora_antiga'), dataFinal('POST', request, 'data_nova_paradas', 'hora_nova'), lista_paradas_maquina2, 2)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_paradas', 'hora_antiga'), dataFinal('POST', request, 'data_nova_paradas', 'hora_nova'), lista_paradas_maquina3, 3)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_paradas', 'hora_antiga'), dataFinal('POST', request, 'data_nova_paradas', 'hora_nova'), lista_paradas_maquina4, 4)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_paradas', 'hora_antiga'), dataFinal('POST', request, 'data_nova_paradas', 'hora_nova'), lista_paradas_maquina5, 5)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_paradas', 'hora_antiga'), dataFinal('POST', request, 'data_nova_paradas', 'hora_nova'), lista_paradas_maquina6, 6)
    
    # 1.4 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        'data_antiga_relatorio': data_antiga_relatorio,
        'hora_antiga_relatorio': hora_antiga_relatorio,
        'data_nova_relatorio': data_nova_relatorio,
        'hora_nova_relatorio': hora_nova_relatorio,
        
        'maquinas': Maquina.objects.all(),                                                          
        
        # MÁQUINAS QUE SERÃO MOSTRADAS COM FILTRO (AS QUE O USUÁRIO SELECIONAR APENAS)
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),                    # 3.4.1 - Comando que busca todas as máquinas cadastradas no banco.

        
        'ultima_atualizacao': datetime.now(),                                                       # 1.4.2 - Variável que conterá a data do último refresh da página.
        'paradas_tipos': Paradas_tipos.objects.all(),                                               # 1.4.3 - Variável que conterá todos os motivos de paradas cadastrados no banco de dados.

        # 1.4.1 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'paradas_maquina1': len(lista_paradas_maquina1),                                            # 1.4.1.1 - Variável que conterá a quantidade de paradas da máquina 1.
        'paradas_maquina2': len(lista_paradas_maquina2),                                            # 1.4.1.2 - Variável que conterá a quantidade de paradas da máquina 3.
        'paradas_maquina3': len(lista_paradas_maquina3),                                            # 1.4.1.3 - Variável que conterá a quantidade de paradas da máquina 4.
        'paradas_maquina4': len(lista_paradas_maquina4),                                            # 1.4.1.4 - Variável que conterá a quantidade de paradas da máquina 5.
        'paradas_maquina5': len(lista_paradas_maquina5),                                            # 1.4.1.5 - Variável que conterá a quantidade de paradas da máquina 6.
        'paradas_maquina6': len(lista_paradas_maquina6),                                            # 1.4.1.6 - Variável que conterá a quantidade de paradas da máquina 7.
        # @MQPARADAS7#
        #'paradas_maquina(id)': len(lista_paradas_maquina5),

        # 1.4.2 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 1
        'parada_motivo1_maquina1': lista_paradas_maquina1.count(1),                                 # 1.4.2.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 1.
        'parada_motivo2_maquina1': lista_paradas_maquina1.count(2),                                 # 1.4.2.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 1.
        'parada_motivo3_maquina1': lista_paradas_maquina1.count(3),                                 # 1.4.2.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 1.
        'parada_motivo4_maquina1': lista_paradas_maquina1.count(4),                                 # 1.4.2.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 1.
        'parada_motivo5_maquina1': lista_paradas_maquina1.count(5),                                 # 1.4.2.1 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 1.

        # 1.4.3 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 3
        'parada_motivo1_maquina2': lista_paradas_maquina2.count(1),                                 # 1.4.3.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 3.
        'parada_motivo2_maquina2': lista_paradas_maquina2.count(2),                                 # 1.4.3.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 3.
        'parada_motivo3_maquina2': lista_paradas_maquina2.count(3),                                 # 1.4.3.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 3.
        'parada_motivo4_maquina2': lista_paradas_maquina2.count(4),                                 # 1.4.3.1 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 3.
        'parada_motivo5_maquina2': lista_paradas_maquina2.count(5),                                 # 1.4.3.1 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 3.

        # 1.4.4 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 4
        'parada_motivo1_maquina3': lista_paradas_maquina3.count(1),                                 # 1.4.4.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 4.
        'parada_motivo2_maquina3': lista_paradas_maquina3.count(2),                                 # 1.4.4.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 4.
        'parada_motivo3_maquina3': lista_paradas_maquina3.count(3),                                 # 1.4.4.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 4.
        'parada_motivo4_maquina3': lista_paradas_maquina3.count(4),                                 # 1.4.4.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 4.
        'parada_motivo5_maquina3': lista_paradas_maquina3.count(5),                                 # 1.4.4.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 4.

        # 1.4.5 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 5
        'parada_motivo1_maquina4': lista_paradas_maquina4.count(1),                                 # 1.4.5.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 5.
        'parada_motivo2_maquina4': lista_paradas_maquina4.count(2),                                 # 1.4.5.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 5.
        'parada_motivo3_maquina4': lista_paradas_maquina4.count(3),                                 # 1.4.5.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 5.
        'parada_motivo4_maquina4': lista_paradas_maquina4.count(4),                                 # 1.4.5.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 5.
        'parada_motivo5_maquina4': lista_paradas_maquina4.count(5),                                 # 1.4.5.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 5.

        # 1.4.6 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 6
        'parada_motivo1_maquina5': lista_paradas_maquina5.count(1),                                 # 1.4.6.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 6.
        'parada_motivo2_maquina5': lista_paradas_maquina5.count(2),                                 # 1.4.6.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 6.
        'parada_motivo3_maquina5': lista_paradas_maquina5.count(3),                                 # 1.4.6.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 6.
        'parada_motivo4_maquina5': lista_paradas_maquina5.count(4),                                 # 1.4.6.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 6.
        'parada_motivo5_maquina5': lista_paradas_maquina5.count(5),                                 # 1.4.6.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 6.

        # 1.4.6 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 7
        'parada_motivo1_maquina6': lista_paradas_maquina6.count(1),                                 # 1.4.7.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 7.
        'parada_motivo2_maquina6': lista_paradas_maquina6.count(2),                                 # 1.4.7.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 7.
        'parada_motivo3_maquina6': lista_paradas_maquina6.count(3),                                 # 1.4.7.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 7.
        'parada_motivo4_maquina6': lista_paradas_maquina6.count(4),                                 # 1.4.7.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 7.
        'parada_motivo5_maquina6': lista_paradas_maquina6.count(5),                                 # 1.4.7.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 7.
        
        # @MQPARADAS8#
        #'parada_motivo1_maquina(id)': lista_paradas_maquina(id).count(1),
        #'parada_motivo2_maquina(id)': lista_paradas_maquina(id).count(2),
        #'parada_motivo3_maquina(id)': lista_paradas_maquina(id).count(3),
        #'parada_motivo4_maquina(id)': lista_paradas_maquina(id).count(4),
        #'parada_motivo5_maquina(id)': lista_paradas_maquina(id).count(5),
    }

    return render(request, 'paradas.html', dados)                                                   # 1.5 - Função que renderiza a página paradas.html com os dados referenciados anteriormente.

