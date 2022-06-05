from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

from dash.views.funcoes.consultas_banco import adicionaProducaoLista
from dash.views.funcoes.filtra_maquinas import filtraMaquinas
from dash.views.funcoes.pega_datas import dataFinal, dataInicial


# 1 - PÁGINA PRODUÇÃO (MENÚ)
def producao(request):
    
                                                         
    data_antiga_producao = str(datetime.now())[:11] + '00:00:01'                                    # 1.1.2 - Data antiga sem filtro.
    data_nova_producao = str(datetime.now()) [:19]                                                  # 1.1.3 - Data nova sem filtro.
    
    lista_producao_producao = []
    adicionaProducaoLista(data_antiga_producao, data_nova_producao, lista_producao_producao)

    maquinas_filtradas = []                                                                         # 1.1.10 - Lista de ids das máquinas a serem exibidas na página Produção (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 1.1.11 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 1.1.11.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)


    data_antiga_relatorio = str(datetime.now())[:11]
    hora_antiga_relatorio = '00:00:01'
    data_nova_relatorio = str(datetime.now())[:11]
    hora_nova_relatorio = str(datetime.now())[11:19]
    
    # 1.2 - PRODUÇÃO DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 1.2.1 - Se houver uma requisição do tipo POST na página...
        data_antiga_relatorio = request.POST.get('data_antiga_producao', False)
        hora_antiga_relatorio = request.POST.get('hora_antiga', False)
        data_nova_relatorio = request.POST.get('data_nova_producao', False)
        hora_nova_relatorio = request.POST.get('hora_nova', False)

        print(data_antiga_relatorio)

        filtraMaquinas('POST', request, maquinas_filtradas)

        data_antiga_producao = dataInicial('POST', request, 'data_antiga_producao', 'hora_antiga')
        data_nova_producao = dataFinal('POST', request, 'data_nova_producao', 'hora_nova')
        
        adicionaProducaoLista(data_antiga_producao, data_nova_producao, lista_producao_producao)

    

        
    # 1.3 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        'data_antiga_relatorio': data_antiga_relatorio,
        'hora_antiga_relatorio': hora_antiga_relatorio,
        'data_nova_relatorio': data_nova_relatorio,
        'hora_nova_relatorio': hora_nova_relatorio,
        
        # MÁQUINAS QUE SERÃO MOSTRADAS SEM FILTRO (TODAS)
        'maquinas': Maquina.objects.all(),
        
        # MÁQUINAS QUE SERÃO MOSTRADAS COM FILTRO (AS QUE O USUÁRIO SELECIONAR APENAS)
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),                    # 1.3.1 - Comando que busca todas as máquinas cadastradas no banco.

        # INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'producao_maquina1': lista_producao_producao.count(1),                                      # 1.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina2': lista_producao_producao.count(2),                                      # 1.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina3': lista_producao_producao.count(3),                                      # 1.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina4': lista_producao_producao.count(4),                                      # 1.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina5': lista_producao_producao.count(5),                                      # 1.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina6': lista_producao_producao.count(6),                                      # 1.3.6 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7
        # @MQPRODUCAO1#
        #'producao_maquina(id da máquina nova)': lista_producao_producao.count(id da máquina nova)  # 1.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7


        'data_antiga': data_antiga_producao,                                                        # 1.3.7 - Variável que contém a data inicial do filtro.
        'data_nova': data_nova_producao,                                                            # 1.3.8 - Variável que contém a data final do filtro.

        'ultima_atualizacao': datetime.now()                                                        # 1.3.9 - Variável que contém a última atualização da página.
    }
    return render(request, 'producao.html', dados)                                                  # 1.4 - Função que renderiza a página producao.html com os dados referenciados anteriormente.

#______________________________________________________________________