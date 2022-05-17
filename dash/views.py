from django.shortcuts import render
from .models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3

#_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# 1 - PÁGINA INDEX 
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

        'ultima_atualizacao': datetime.now()                                                        # 1.4.7 - Função que pega a data e o horário atual para indicar a última atualização.
 
    }

    return render(request, 'index.html', dados)                                                     # 1.5 Função que renderiza a página index.html com os dados referenciados anteriormente.

#_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# 2 - PÁGINA GERAL (MENÚ)
def geral(request):

    # 2.1 - LISTAS UTILIZADAS NA PÁGINA
    lista_producao_geral = []                                                                       # 2.1.1 - Lista que contem todos os registros de produção de todas as máquinas.
    lista_paradas_geral = []                                                                        # 2.1.2 - Lista que contem todos os registros de paradas de todas as máquinas.
    
    # 2.2 - INÍCIO DA CONEXÃO COM O BANCO E CAPTURA DAS DATAS SEM FILTRO
    data_antiga_geral = str(datetime.now())[:11] + '00:00:01'                                       # 2.2.1 - Data antiga sem filtro.
    data_nova_geral = str(datetime.now()) [:19]                                                     # 2.2.2 - Data nova sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                                      # 2.2.3 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 2.2.4 - Cursor que receberá os comandos do banco de dados.
    
    # 2.3 - CONEXÃO E CAPTURA DE REGISTROS DE PRODUÇÃO SEM FILTTO
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_geral, data_nova_geral)) # 2.3.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result_producao = cursor.fetchall()                                                             # 2.3.2 - Resultado da filtragem padrão.
    lista_producao_geral.clear()                                                                    # 2.3.3 - Função que limpará a lista antes de adquirir dados novos.
    for i in result_producao:                                                                       # 2.3.4 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao_geral.append(i[0])                                                           # 2.3.4.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    # 2.4 - CONEXÃO E CAPTURA DE REGISTROS DE PARADAS SEM FILTRO
    cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_geral, data_nova_geral)) # 2.4.1 - Cursor com o comando que filtrará os registros de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result_paradas = cursor.fetchall()                                                              # 2.4.2 - Resultado da filtragem padrão.
    for i in result_paradas:                                                                        # 2.4.3 - Loop que percorrerá os dados de paradas e adicionará na lista de paradas.
        lista_paradas_geral.append(i[0])                                                            # 2.4.3.1 - Função que adicionará na lista de paradas geral o primeiro item da lista retornada do banco.
    
    # 2.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 2.5.1 - Se houver uma requisição do tipo POST na página...
        data_antiga_geral = request.POST.get('data_antiga_geral', False) + ' ' + request.POST.get('hora_antiga', False)   # 2.5.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_geral = request.POST.get('data_nova_geral', False) + ' ' + request.POST.get('hora_nova', False)         # 2.5.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 2.5.4 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 2.5.5 - Cursor que receberá os comandos SQL.
        
        # 2.5.6 - PRODUÇÃO DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_geral, data_nova_geral)) # 2.5.6.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        lista_producao_geral.clear()                                                                # 2.5.6.2 - Função que limpará a lista antes de adquirir dados novos.
        result = cursor.fetchall()                                                                  # 2.5.6.3 - Resultado da filtragem realizada anteriormente pelo usuário.
        for i in result:                                                                            # 2.5.6.4 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_geral.append(i[0])                                                       # 2.5.6.4.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

        # 2.5.7 - PARADAS DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_geral, data_nova_geral)) # 2.5.7.1 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
        result_paradas = cursor.fetchall()                                                          # 2.5.7.2 - Resultado da filtragem padrão.
        for i in result_paradas:                                                                    # 2.5.7.3 - Loop que percorrerá os dados de paradas e adicionará na lista de paradas.
            lista_paradas_geral.append(i[0])                                                        # 2.5.7.3.1 - Função que adicionará na lista de paradas geral o primeiro item da lista retornada do banco.


    # 2.6 - INÍCIO DOS DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        'maquinas': Maquina.objects.all(),                                                          # 2.6.1 - Variável com comando que busca todas as máquinas cadastradas no banco.

        # 2.6.2 - INÍCIO DAS MÁQUINAS NA PÁGINA GERAL
        'maquina1': Maquina.objects.get(id=1),                                                      # 2.6.2.1 - Buscando o nome da máquina 1 no banco.
        'maquina3': Maquina.objects.get(id=3),                                                      # 2.6.2.2 - Buscando o nome da máquina 3 no banco.
        'maquina4': Maquina.objects.get(id=4),                                                      # 2.6.2.3 - Buscando o nome da máquina 4 no banco.
        'maquina5': Maquina.objects.get(id=5),                                                      # 2.6.2.4 - Buscando o nome da máquina 5 no banco.

        # 2.6.3 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS
        'producao_maquina1': lista_producao_geral.count(1),                                         # 2.6.3.1 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_geral.count(3),                                         # 2.6.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_geral.count(4),                                         # 2.6.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_geral.count(5),                                         # 2.6.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5

        # 2.6.4 - INÍCIO DADOS DE PARADAS DAS MÁQUINAS
        'paradas_maquina1': lista_paradas_geral.count(1),                                           # 2.6.4.1 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 1
        'paradas_maquina3': lista_paradas_geral.count(3),                                           # 2.6.4.2 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 3
        'paradas_maquina4': lista_paradas_geral.count(4),                                           # 2.6.4.3 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 4
        'paradas_maquina5': lista_paradas_geral.count(5),                                           # 2.6.4.4 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5

        'ultima_atualizacao': datetime.now()                                                        # 2.6.4.5 - Variável que pega a data e hora do último refresh na página.
    }

    return render(request, 'geral.html', dados)                                                     # 3 - Função que renderiza a página geral.html com os dados referenciados anteriormente.

#_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
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
    
    maquinas_filtradas = []                                                                         # 1.2.9 - Lista de ids das máquinas a serem exibidas na página inicial (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 1.2.10 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 1.2.10.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)


    # 3.2 - PRODUÇÃO DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 3.2.1 - Se houver uma requisição do tipo POST na página...
        
        maquinas_filtradas = []                                                                     # 1.3.2 - Lista de máquinas com filtro...
        for maquina in Maquina.objects.values('id'):                                                # 1.3.3 - Loop que percorrerá todas as máquinas cadastradas no banco...
            maquina_filtrada = request.POST.get('filtro_{}'.format(maquina['id']), False)           # 1.3.3.1 - Bucando os valores filtrados no index.
            print(maquina_filtrada)
            if maquina_filtrada != False:                                                           # 1.3.3.2 - Se o valor recebido for diferente de False...
                maquinas_filtradas.append(maquina_filtrada)                                         # 1.3.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)
        print(maquinas_filtradas)
        data_antiga_producao = request.POST.get('data_antiga_producao', False) + ' ' + request.POST.get('hora_antiga', False)   # 3.2.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_producao = request.POST.get('data_nova_producao', False) + ' ' + request.POST.get('hora_nova', False)         # 3.2.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 3.2.4 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 3.2.5 - Cursor que receberá os comandos SQL.
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_producao, data_nova_producao)) # 3.2.6 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        lista_producao_producao.clear()                                                             # 3.2.7 - Função que limpará a lista antes de adquirir dados novos.
        result = cursor.fetchall()                                                                  # 3.2.8 - Resultado da filtragem realizada anteriormente pelo usuário.
        for i in result:                                                                            # 3.2.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_producao.append(i[0])                                                    # 3.2.9.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    # 3.3 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {
        
        # MÁQUINAS QUE SERÃO MOSTRADAS SEM FILTRO (TODAS)
        'maquinas': Maquina.objects.all(),
        
        # MÁQUINAS QUE SERÃO MOSTRADAS COM FILTRO (AS QUE O USUÁRIO SELECIONAR APENAS)
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),                    # 1.4.1 - Comando que busca todas as máquinas cadastradas no banco.

        # INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'producao_maquina1': lista_producao_producao.count(1),                                      # 3.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_producao.count(3),                                      # 3.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_producao.count(4),                                      # 3.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_producao.count(5),                                      # 3.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5

        'data_antiga': data_antiga_producao,                                                        # 3.3.6 - Variável que contém a data inicial do filtro.
        'data_nova': data_nova_producao,                                                            # 3.3.7 - Variável que contém a data final do filtro.

        'ultima_atualizacao': datetime.now()                                                        # 3.3.8 - Variável que contém a última atualização da página.
    }
    return render(request, 'producao.html', dados)                                                  # 3.4 - Função que renderiza a página producao.html com os dados referenciados anteriormente.

#_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________
# 4 - PÁGINA PARADAS (MENÚ)
def paradas(request):

    # 4.1 - LISTA DE PARADAS POR MÁQUINA
    lista_paradas_maquina1 = []                                                                     # 4.1.1 - Contém todas as paradas da máquina 1
    lista_paradas_maquina3 = []                                                                     # 4.1.2 - Contém todas as paradas da máquina 3
    lista_paradas_maquina4 = []                                                                     # 4.1.4 - Contém todas as paradas da máquina 4
    lista_paradas_maquina5 = []                                                                     # 4.1.5 - Contém todas as paradas da máquina 5

    if len(lista_paradas_maquina1) > 0:                                                             # 4.1.6 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina1 = lista_paradas_maquina1.sort()                                      # 4.1.6.1 - Ordenando a lista.
    if len(lista_paradas_maquina3) > 0:                                                             # 4.1.7 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina3 = lista_paradas_maquina1.sort()                                      # 4.1.7.1 - Ordenando a lista.
    if len(lista_paradas_maquina4) > 0:                                                             # 4.1.8 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina4 = lista_paradas_maquina1.sort()                                      # 4.1.8.1 - Ordenando a lista.
    if len(lista_paradas_maquina5) > 0:                                                             # 4.1.9 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina5 = lista_paradas_maquina1.sort()                                      # 4.1.9.1 - Ordenando a lista.

    # 4.2 - PARADAS DAS MÁQUINAS SEM FILTRO
    lista_paradas = []                                                                              # 4.2.1 - Lista com todas as paradas de todas as máquinas.
    data_antiga_paradas = str(datetime.now())[:11] + '00:00:01'                                     # 4.2.2 - Data antiga sem filtro.
    data_nova_paradas = str(datetime.now()) [:19]                                                   # 4.2.3 - Data nova sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                                      # 4.2.4 - Função que realiza a conexão com o banco Sqlite.
    cursor = connection.cursor()                                                                    # 4.2.5 - Cursor que receberá todos os comandos que serão executados no banco de dados.
    cursor.execute("SELECT * FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_paradas, data_nova_paradas)) # 4.2.6 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 4.2.7 - Resultado obtido da consulta realizada no banco.
    lista_paradas_maquina1.clear()                                                                  # 4.2.8 - Limpando a lista de paradas da máquina 1.
    lista_paradas_maquina3.clear()                                                                  # 4.2.9 - Limpando a lista de paradas da máquina 3.
    lista_paradas_maquina4.clear()                                                                  # 4.2.10 - Limpando a lista de paradas da máquina 4.
    lista_paradas_maquina5.clear()                                                                  # 4.2.11 - Limpando a lista de paradas da máquina 5.
    for i in result:                                                                                # 4.2.12 - Loop que percorrerá todos os itens do resultado obtido na consulta realizada no banco de dados.
        if i[2] == 1:                                                                               # 4.2.12.1 - Se o terceiro item da lista percorrida for igual a 1...
            lista_paradas_maquina1.append(i[3])                                                     # 4.2.12.1.1 - Adiciona o item encontrado na lista de paradas da máquina 1.
        elif i[2] == 3:                                                                             # 4.2.12.2 - Se o terceiro item da lista percorrida for igual a 3...
            lista_paradas_maquina3.append(i[3])                                                     # 4.2.12.2.1 - Adiciona o item encontrado na lista de paradas da máquina 3.
        elif i[2] == 4:                                                                             # 4.2.12.3 - Se o terceiro item da lista percorrida for igual a 4...
            lista_paradas_maquina4.append(i[3])                                                     # 4.2.12.3.1 - Adiciona o tem encontrado na lista de paradas da máquina 4.
        elif i[2] == 5:                                                                             # 4.2.12.4 - Se o terceiro item da lista percorrida for igual a 5...
            lista_paradas_maquina5.append(i[3])                                                     # 4.2.12.4.1 - Adiciona o item encontrado na lista de paradas da máquina 5.
    
    # 4.3 - PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 4.3.1 - Se houver uma requisição do tipo POST na página...
        data_antiga_paradas = request.POST.get('data_antiga_paradas', False) + ' ' + request.POST.get('hora_antiga', False)     # 4.3.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_paradas = request.POST.get('data_nova_paradas', False) + ' ' + request.POST.get('hora_nova', False)           # 4.3.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 4.3.4 - Comando que realizada a conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 4.3.5 - Cursor que receberá todos os comandos que serão executados no banco de dados.
        cursor.execute("SELECT * FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_paradas, data_nova_paradas)) # 4.3.6 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        result = cursor.fetchall()                                                                  # 4.3.7 - Resultado obtido do banco de dados.
        lista_paradas_maquina1.clear()                                                              # 4.3.8 - Limpando a lista de paradas da máquina 1.
        lista_paradas_maquina3.clear()                                                              # 4.3.9 - Limpando a lista de paradas da máquina 3.
        lista_paradas_maquina4.clear()                                                              # 4.3.10 - Limpando a lista de paradas da máquina 4.
        lista_paradas_maquina5.clear()                                                              # 4.3.11 - Limpando a lista de paradas da máquina 5.
        for i in result:                                                                            # 4.3.12 - Loop que percorrerá todos os itens do resultado obtido na consulta realizada no banco de dados.
            if i[2] == 1:                                                                           # 4.3.12.1 - Se o terceiro item da lista percorrida for igual a 1...
                lista_paradas_maquina1.append(i[3])                                                 # 4.3.12.1.1 - Adiciona o item encontrado na lista de paradas da máquina 1.
            elif i[2] == 3:                                                                         # 4.3.12.2 - Se o terceiro item da lista percorrida for igual a 3...
                lista_paradas_maquina3.append(i[3])                                                 # 4.3.12.2.1 - Adiciona o item encontrado na lista de paradas da máquina 3.
            elif i[2] == 4:                                                                         # 4.3.12.3 - Se o terceiro item da lista percorrida for igual a 4...
                lista_paradas_maquina4.append(i[3])                                                 # 4.3.12.3.1 - Adiciona o tem encontrado na lista de paradas da máquina 4.
            elif i[2] == 5:                                                                         # 4.3.12.4 - Se o terceiro item da lista percorrida for igual a 5...
                lista_paradas_maquina5.append(i[3])                                                 # 4.3.12.4.1 - Adiciona o item encontrado na lista de paradas da máquina 5.

    # 4.4 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {
        'maquinas': Maquina.objects.all(),                                                          # 4.4.1 - Variável que conterá todas as máquinas cadastradas no banco.
        'ultima_atualizacao': datetime.now(),                                                       # 4.4.2 - Variável que conterá a data do último refresh da página.
        'paradas_tipos': Paradas_tipos.objects.all(),                                               # 4.4.3 - Variável que conterá todos os motivos de paradas cadastrados no banco de dados.

        # 4.4.1 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'paradas_maquina1': len(lista_paradas_maquina1),                                            # 4.4.1.1 - Variável que conterá a quantidade de paradas da máquina 1.
        'paradas_maquina3': len(lista_paradas_maquina3),                                            # 4.4.1.2 - Variável que conterá a quantidade de paradas da máquina 3.
        'paradas_maquina4': len(lista_paradas_maquina4),                                            # 4.4.1.3 - Variável que conterá a quantidade de paradas da máquina 4.
        'paradas_maquina5': len(lista_paradas_maquina5),                                            # 4.4.1.4 - Variável que conterá a quantidade de paradas da máquina 5.

        # 4.4.2 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 1
        'parada_motivo1_maquina1': lista_paradas_maquina1.count(1),                                 # 4.4.2.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 1.
        'parada_motivo2_maquina1': lista_paradas_maquina1.count(2),                                 # 4.4.2.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 1.
        'parada_motivo3_maquina1': lista_paradas_maquina1.count(3),                                 # 4.4.2.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 1.
        'parada_motivo4_maquina1': lista_paradas_maquina1.count(4),                                 # 4.4.2.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 1.
        'parada_motivo5_maquina1': lista_paradas_maquina1.count(5),                                 # 4.4.2.1 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 1.

        # 4.4.3 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 3
        'parada_motivo1_maquina3': lista_paradas_maquina3.count(1),                                 # 4.4.3.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 3.
        'parada_motivo2_maquina3': lista_paradas_maquina3.count(2),                                 # 4.4.3.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 3.
        'parada_motivo3_maquina3': lista_paradas_maquina3.count(3),                                 # 4.4.3.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 3.
        'parada_motivo4_maquina3': lista_paradas_maquina3.count(4),                                 # 4.4.3.1 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 3.
        'parada_motivo5_maquina3': lista_paradas_maquina3.count(5),                                 # 4.4.3.1 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 3.

        # 4.4.4 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 4
        'parada_motivo1_maquina4': lista_paradas_maquina4.count(1),                                 # 4.4.4.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 4.
        'parada_motivo2_maquina4': lista_paradas_maquina4.count(2),                                 # 4.4.4.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 4.
        'parada_motivo3_maquina4': lista_paradas_maquina4.count(3),                                 # 4.4.4.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 4.
        'parada_motivo4_maquina4': lista_paradas_maquina4.count(4),                                 # 4.4.4.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 4.
        'parada_motivo5_maquina4': lista_paradas_maquina4.count(5),                                 # 4.4.4.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 4.

        # 4.4.5 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 5
        'parada_motivo1_maquina5': lista_paradas_maquina5.count(1),                                 # 4.4.5.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 5.
        'parada_motivo2_maquina5': lista_paradas_maquina5.count(2),                                 # 4.4.5.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 5.
        'parada_motivo3_maquina5': lista_paradas_maquina5.count(3),                                 # 4.4.5.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 5.
        'parada_motivo4_maquina5': lista_paradas_maquina5.count(4),                                 # 4.4.5.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 5.
        'parada_motivo5_maquina5': lista_paradas_maquina5.count(5),                                 # 4.4.5.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 5.

    }

    return render(request, 'paradas.html', dados)                                                   # 4.5 - Função que renderiza a página paradas.html com os dados referenciados anteriormente.

#_______________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________________