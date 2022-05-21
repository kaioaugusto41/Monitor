from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse


# 3 - PÁGINA PRODUÇÃO (MENÚ)
def producao(request):
    
    # 3.1 - PRODUÇÃO DAS MÁQUINAS SEM FILTRO
    lista_producao_producao = []                                                                    # 3.1.1 - Lista que contem todos os registros de produção de todas as máquinas.
    data_antiga_producao = str(datetime.now())[:11] + '00:00:01'                                    # 3.1.2 - Data antiga sem filtro.
    data_nova_producao = str(datetime.now()) [:19]                                                  # 3.1.3 - Data nova sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                                      # 3.1.4 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 3.1.5 - Cursor que receberá os comandos do banco de dados.
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_producao, data_nova_producao)) # 3.1.6 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 3.1.7 - Resultado da filtragem padrão.
    lista_producao_producao.clear()                                                                 # 3.1.8 - Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                                # 3.1.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao_producao.append(i[0])                                                        # 3.1.9.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.
    
    maquinas_filtradas = []                                                                         # 3.1.10 - Lista de ids das máquinas a serem exibidas na página Produção (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 3.1.11 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 3.1.11.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)


    # 3.2 - PRODUÇÃO DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 3.2.1 - Se houver uma requisição do tipo POST na página...
        
        maquinas_filtradas = []                                                                     # 3.2.2 - Lista de máquinas com filtro...
        for maquina in Maquina.objects.values('id'):                                                # 3.2.3 - Loop que percorrerá todas as máquinas cadastradas no banco...
            maquina_filtrada = request.POST.get('filtro_{}'.format(maquina['id']), False)           # 3.2.3.1 - Bucando os valores filtrados no index.
            if maquina_filtrada != False:                                                           # 3.2.3.2 - Se o valor recebido for diferente de False...
                maquinas_filtradas.append(maquina_filtrada)                                         # 3.2.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)
        data_antiga_producao = request.POST.get('data_antiga_producao', False) + ' ' + request.POST.get('hora_antiga', False)   # 3.2.4 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_producao = request.POST.get('data_nova_producao', False) + ' ' + request.POST.get('hora_nova', False)         # 3.2.5 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 3.2.6 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 3.2.7 - Cursor que receberá os comandos SQL.
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_producao, data_nova_producao)) # 3.2.8 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        lista_producao_producao.clear()                                                             # 3.2.9 - Função que limpará a lista antes de adquirir dados novos.
        result = cursor.fetchall()                                                                  # 3.2.10 - Resultado da filtragem realizada anteriormente pelo usuário.
        for i in result:                                                                            # 3.2.11 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_producao.append(i[0])                                                    # 3.2.11.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    # 3.3 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {
        
        # MÁQUINAS QUE SERÃO MOSTRADAS SEM FILTRO (TODAS)
        'maquinas': Maquina.objects.all(),
        
        # MÁQUINAS QUE SERÃO MOSTRADAS COM FILTRO (AS QUE O USUÁRIO SELECIONAR APENAS)
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),                    # 3.3.1 - Comando que busca todas as máquinas cadastradas no banco.

        # INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'producao_maquina1': lista_producao_producao.count(1),                                      # 3.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_producao.count(3),                                      # 3.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_producao.count(4),                                      # 3.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_producao.count(5),                                      # 3.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina6': lista_producao_producao.count(6),                                      # 3.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina7': lista_producao_producao.count(7),                                      # 3.3.6 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7
        # @MQPRODUCAO1#
        #'producao_maquina(id da máquina nova)': lista_producao_producao.count(id da máquina nova)  # 3.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7


        'data_antiga': data_antiga_producao,                                                        # 3.3.7 - Variável que contém a data inicial do filtro.
        'data_nova': data_nova_producao,                                                            # 3.3.8 - Variável que contém a data final do filtro.

        'ultima_atualizacao': datetime.now()                                                        # 3.3.9 - Variável que contém a última atualização da página.
    }
    return render(request, 'producao.html', dados)                                                  # 3.4 - Função que renderiza a página producao.html com os dados referenciados anteriormente.

#______________________________________________________________________