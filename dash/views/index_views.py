from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def index(request):

    # 1.1 - REQUISIÇÃO DA EDIÇÃO DOS NOMES DAS MÁQUINAS 
    if request.method == 'GET':                                                                     # 1.1.1 - Se houver uma requisição do tipo GET na página...
        nome_maquina_antigo = request.GET.get('nome_maquina_antigo', False)                         # 1.1.2 - Nome da máquina antes de ser renomeada.
        nome_maquina_novo = request.GET.get('nome_maquina_novo', False)                             # 1.1.3 - Nome da máquina após ser renomeada.
        maquina_a_renomear  = Maquina.objects.filter(nome_maquina=nome_maquina_antigo).update(nome_maquina=nome_maquina_novo)  # 1.1.4 - Comando para alterar o nome da máquina no banco de dados.
  

    # 1.2 - PRODUÇÃO DAS MÁQUINAS SEM FILTRO (PADRÃO)
    lista_producao_index = []                                                                       # 1.2.1 - Lista que contém todas as produções de todas as máquinas.
    data_antiga_index = str(datetime.now())[:11] + '00:00:01'                                       # 1.2.2 - Data antiga sem filtro.
    data_nova_index = str(datetime.now())[:19]                                                      # 1.2.3 - Data atual sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                                      # 1.2.4 - Comando de conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 1.2.5 - Cursor que receberá os comandos SQL.
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_index, data_nova_index))  # 1.2.6 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 1.2.6 - Resultado da filtragem padrão.
    lista_producao_index.clear()                                                                    # 1.2.7 - Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                                # 1.2.8 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao_index.append(i[0])                                                           # 1.2.8.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.
    
    maquinas_filtradas = []                                                                         # 1.2.9 - Lista de ids das máquinas a serem exibidas na página inicial (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 1.2.10 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 1.2.10.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)

    # 1.3 - PRODUÇÃO DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 1.3.1 - Se houver uma requisição do tipo POST na página...
        maquinas_filtradas = []                                                                     # 1.3.2 - Lista de máquinas com filtro...
        for maquina in Maquina.objects.values('id'):                                                # 1.3.3 - Loop que percorrerá todas as máquinas cadastradas no banco...
            maquina_filtrada = request.POST.get('filtro_{}'.format(maquina['id']), False)           # 1.3.3.1 - Bucando os valores filtrados no index.
            if maquina_filtrada != False:                                                           # 1.3.3.2 - Se o valor recebido for diferente de False...
                maquinas_filtradas.append(maquina_filtrada)                                         # 1.3.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)
        
        data_antiga_index = request.POST.get('data_antiga_index', False) + ' ' + request.POST.get('hora_antiga', False)     # 1.3.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_index = request.POST.get('data_nova_index', False) + ' ' + request.POST.get('hora_nova', False)           # 1.3.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 1.3.4 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 1.3.5 - Cursor que receberá os comandos SQL.
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_index, data_nova_index)) # 1.3.6 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        result = cursor.fetchall()                                                                  # 1.3.7 - Resultado da filtragem realizada anteriormente pelo usuário.
        lista_producao_index.clear()                                                                # 1.3.8 - Função que limpará a lista antes de adquirir dados novos.
        for i in result:                                                                            # 1.3.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_index.append(i[0])                                                       # 1.3.9.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

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
