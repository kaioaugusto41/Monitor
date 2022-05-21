from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3


# 2 - PÁGINA GERAL (MENÚ)
def geral(request):

    # 2.1 - LISTAS UTILIZADAS NA PÁGINA
    lista_producao_geral = []                                                                      # 2.1.1 - Lista que contem todos os registros de produção de todas as máquinas.
    lista_paradas_geral = []                                                                       # 2.1.2 - Lista que contem todos os registros de paradas de todas as máquinas.
    
    # 2.2 - INÍCIO DA CONEXÃO COM O BANCO E CAPTURA DAS DATAS SEM FILTRO
    data_antiga_maquina = str(datetime.now())[:11] + '00:00:01'                                      # 2.2.1 - Data antiga sem filtro.
    data_nova_maquina = str(datetime.now()) [:19]                                                    # 2.2.2 - Data nova sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                                       # 2.2.3 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                     # 2.2.4 - Cursor que receberá os comandos do banco de dados.
    
    # 2.3 - CONEXÃO E CAPTURA DE REGISTROS DE PRODUÇÃO SEM FILTTO
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_maquina, data_nova_maquina)) # 2.3.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result_producao = cursor.fetchall()                                                              # 2.3.2 - Resultado da filtragem padrão.
    lista_producao_geral.clear()                                                                   # 2.3.3 - Função que limpará a lista antes de adquirir dados novos.
    for i in result_producao:                                                                        # 2.3.4 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao_geral.append(i[0])                                                          # 2.3.4.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    # 2.4 - CONEXÃO E CAPTURA DE REGISTROS DE PARADAS SEM FILTRO
    cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_maquina, data_nova_maquina)) # 2.4.1 - Cursor com o comando que filtrará os registros de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result_paradas = cursor.fetchall()                                                               # 2.4.2 - Resultado da filtragem padrão.
    lista_paradas_geral.clear()                                                                    # 2.4.3 - Função que limpará a lista antes de adquirir dados novos.
    for i in result_paradas:                                                                         # 2.4.4 - Loop que percorrerá os dados de paradas e adicionará na lista de paradas.
        lista_paradas_geral.append(i[0])                                                           # 2.4.4.1 - Função que adicionará na lista de paradas geral o primeiro item da lista retornada do banco.
    
    # 2.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                     # 2.5.1 - Se houver uma requisição do tipo POST na página...
        data_antiga_geral = request.POST.get('data_antiga_geral', False) + ' ' + request.POST.get('hora_antiga', False)   # 2.5.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_geral = request.POST.get('data_nova_geral', False) + ' ' + request.POST.get('hora_nova', False)         # 2.5.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                   # 2.5.4 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                 # 2.5.5 - Cursor que receberá os comandos SQL.
        
        # 2.5.6 - PRODUÇÃO DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_geral, data_nova_geral)) # 2.5.6.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        lista_producao_geral.clear()                                                               # 2.5.6.2 - Função que limpará a lista antes de adquirir dados novos.
        result = cursor.fetchall()                                                                   # 2.5.6.3 - Resultado da filtragem realizada anteriormente pelo usuário.
        lista_producao_geral.clear()                                                               # 2.5.6.4 - Função que limpará a lista antes de adquirir dados novos.
        for i in result:                                                                             # 2.5.6.5 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_geral.append(i[0])                                                      # 2.5.6.5.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

        # 2.5.7 - PARADAS DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_geral, data_nova_geral)) # 2.5.7.1 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
        result_paradas = cursor.fetchall()                                                           # 2.5.7.2 - Resultado da filtragem padrão.
        lista_paradas_geral.clear()                                                                # 2.5.7.3 - Função que limpará a lista antes de adquirir dados novos.
        for i in result_paradas:                                                                     # 2.5.7.4 - Loop que percorrerá os dados de paradas e adicionará na lista de paradas.
            lista_paradas_geral.append(i[0])                                                       # 2.5.7.4.1 - Função que adicionará na lista de paradas geral o primeiro item da lista retornada do banco.


    # 2.6 - INÍCIO DOS DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {

        'maquinas': Maquina.objects.all(),                                                          # 2.6.1 - Variável com comando que busca todas as máquinas cadastradas no banco.

        # 2.6.2 - INÍCIO DAS MÁQUINAS NA PÁGINA GERAL
        'maquina1': Maquina.objects.get(id=1),                                                      # 2.6.2.1 - Buscando o nome da máquina 1 no banco.
        'maquina3': Maquina.objects.get(id=3),                                                      # 2.6.2.2 - Buscando o nome da máquina 3 no banco.
        'maquina4': Maquina.objects.get(id=4),                                                      # 2.6.2.3 - Buscando o nome da máquina 4 no banco.
        'maquina5': Maquina.objects.get(id=5),                                                      # 2.6.2.4 - Buscando o nome da máquina 5 no banco.
        'maquina6': Maquina.objects.get(id=6),                                                      # 2.6.2.5 - Buscando o nome da máquina 6 no banco.
        'maquina7': Maquina.objects.get(id=7),                                                      # 2.6.2.6 - Buscando o nome da máquina 7 no banco.
        # @MQGERAL1#
        #'maquina5': Maquina.objects.get(id=id da máquina nova),                                    # 2.6.2.7 - Buscando o nome da máquina 5 no banco.

        # 2.6.3 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS
        'producao_maquina1': lista_producao_geral.count(1),                                        # 2.6.3.1 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_geral.count(3),                                        # 2.6.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_geral.count(4),                                        # 2.6.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_geral.count(5),                                        # 2.6.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina6': lista_producao_geral.count(6),                                        # 2.6.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina7': lista_producao_geral.count(7),                                        # 2.6.3.6 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7 
        # @MQGERAL2#
        #'producao_maquina5': lista_producao_geral.count(id da máquina nova),                      # 2.6.3.7 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        
        # 2.6.4 - INÍCIO DADOS DE PARADAS DAS MÁQUINAS
        'paradas_maquina1': lista_paradas_geral.count(1),                                          # 2.6.4.1 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 1
        'paradas_maquina3': lista_paradas_geral.count(3),                                          # 2.6.4.2 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 3
        'paradas_maquina4': lista_paradas_geral.count(4),                                          # 2.6.4.3 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 4
        'paradas_maquina5': lista_paradas_geral.count(5),                                          # 2.6.4.4 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
        'paradas_maquina6': lista_paradas_geral.count(6),                                          # 2.6.4.5 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 6
        'paradas_maquina7': lista_paradas_geral.count(7),                                          # 2.6.4.6 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 7   
        #@MQGERAL3#
        #'paradas_maquina5': lista_paradas_geral.count(id da máquina nova),                        # 2.6.4.7 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
        
        'ultima_atualizacao': datetime.now()                                                         # 2.6.4.8 - Variável que pega a data e hora do último refresh na página.
    }

    return render(request, 'geral.html', dados)                                                      # 3 - Função que renderiza a página geral.html com os dados referenciados anteriormente.
