from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse



# 5 - PÁGINA DE CADA MÁQUINA (MENÚ)
def maquina(request, id_maquina):

    # 5.1 - LISTAS UTILIZADAS NA PÁGINA
    lista_producao_maquina = []                                                                     # 5.1.1 - Lista que contem todos os registros de produção de todas as máquinas.
    lista_paradas_maquina = []                                                                      # 5.1.2 - Lista que contem todos os registros de paradas de todas as máquinas.
    
    # 5.2 - INÍCIO DA CONEXÃO COM O BANCO E CAPTURA DAS DATAS SEM FILTRO
    data_antiga_maquina = str(datetime.now())[:11] + '00:00:01'                                     # 5.2.1 - Data antiga sem filtro.
    data_nova_maquina = str(datetime.now()) [:19]                                                   # 5.2.2 - Data nova sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                                      # 5.2.3 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 5.2.4 - Cursor que receberá os comandos do banco de dados.
    
    # 5.3 - CONEXÃO E CAPTURA DE REGISTROS DE PRODUÇÃO SEM FILTTO
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_maquina, data_nova_maquina)) # 5.3.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result_producao = cursor.fetchall()                                                             # 5.3.2 - Resultado da filtragem padrão.
    lista_producao_maquina.clear()                                                                  # 5.3.3 - Função que limpará a lista antes de adquirir dados novos.
    for i in result_producao:                                                                       # 5.3.4 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao_maquina.append(i[0])                                                         # 5.3.4.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    # 5.4 - CONEXÃO E CAPTURA DE REGISTROS DE PARADAS SEM FILTRO
    cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_maquina, data_nova_maquina)) # 5.4.1 - Cursor com o comando que filtrará os registros de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result_paradas = cursor.fetchall()                                                              # 5.4.2 - Resultado da filtragem padrão.
    lista_paradas_maquina.clear()                                                                   # 5.4.3 - Função que limpará a lista antes de adquirir dados novos.
    for i in result_paradas:                                                                        # 5.4.4 - Loop que percorrerá os dados de paradas e adicionará na lista de paradas.
        lista_paradas_maquina.append(i[0])                                                          # 5.4.4.1 - Função que adicionará na lista de paradas geral o primeiro item da lista retornada do banco.
    
    # 5.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 5.5.1 - Se houver uma requisição do tipo POST na página...
        print('***********', request.POST.get('data_nova_maquina', False))
        data_antiga_maquina = request.POST.get('data_antiga_maquina', False) + ' ' + request.POST.get('hora_antiga_maquina', False)   # 5.5.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_maquina = request.POST.get('data_nova_maquina', False) + ' ' + request.POST.get('hora_nova_maquina', False)         # 5.5.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 5.5.4 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 5.5.5 - Cursor que receberá os comandos SQL.
        
        # 5.5.6 - PRODUÇÃO DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_maquina, data_nova_maquina)) # 5.5.6.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        lista_producao_maquina.clear()                                                              # 5.5.6.2 - Função que limpará a lista antes de adquirir dados novos.
        result = cursor.fetchall()                                                                  # 5.5.6.3 - Resultado da filtragem realizada anteriormente pelo usuário.
        lista_producao_maquina.clear()                                                              # 5.5.6.4 - Função que limpará a lista antes de adquirir dados novos.
        for i in result:                                                                            # 5.5.6.5 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_maquina.append(i[0])                                                     # 5.5.6.5.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

        # 5.5.7 - PARADAS DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_maquina, data_nova_maquina)) # 5.5.7.1 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
        result_paradas = cursor.fetchall()                                                          # 5.5.7.2 - Resultado da filtragem padrão.
        lista_paradas_maquina.clear()                                                               # 5.5.7.3 - Função que limpará a lista antes de adquirir dados novos.
        for i in result_paradas:                                                                    # 5.5.7.4 - Loop que percorrerá os dados de paradas e adicionará na lista de paradas.
            lista_paradas_maquina.append(i[0])                                                      # 5.5.7.4.1 - Função que adicionará na lista de paradas geral o primeiro item da lista retornada do banco.

    dados = {
        'maquina': get_object_or_404(Maquina, pk=id_maquina),
        'maquinas': Maquina.objects.all(),
        'motivos_paradas': Paradas_tipos.objects.all(),

        # 5.6.2 - INÍCIO DAS MÁQUINAS NA PÁGINA GERAL
        'maquina1': Maquina.objects.get(id=1),                                                      # 5.6.2.1 - Buscando o nome da máquina 1 no banco.
        'maquina3': Maquina.objects.get(id=3),                                                      # 5.6.2.2 - Buscando o nome da máquina 3 no banco.
        'maquina4': Maquina.objects.get(id=4),                                                      # 5.6.2.3 - Buscando o nome da máquina 4 no banco.
        'maquina5': Maquina.objects.get(id=5),                                                      # 5.6.2.4 - Buscando o nome da máquina 5 no banco.
        'maquina6': Maquina.objects.get(id=6),                                                      # 5.6.2.5 - Buscando o nome da máquina 6 no banco.
        'maquina7': Maquina.objects.get(id=7),                                                      # 5.6.2.6 - Buscando o nome da máquina 7 no banco.
        # @MQMAQUINA1#
        #'maquina5': Maquina.objects.get(id=id da máquina nova),                                    # 5.6.2.7 - Buscando o nome da máquina 5 no banco.

        # 5.6.3 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS
        'producao_maquina1': lista_producao_maquina.count(1),                                       # 5.6.3.1 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_maquina.count(3),                                       # 5.6.3.2 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_maquina.count(4),                                       # 5.6.3.3 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_maquina.count(5),                                       # 5.6.3.4 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        'producao_maquina6': lista_producao_maquina.count(6),                                       # 5.6.3.5 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 6
        'producao_maquina7': lista_producao_maquina.count(7),                                       # 5.6.3.6 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 7 
        # @MQMAQUINA2#
        #'producao_maquina5': lista_producao_maquina.count(id da máquina nova),                     # 5.6.3.7 - Variável que conta quantas peças foram produzidas no período filtrado na máquina com o ID 5
        
        # 5.6.4 - INÍCIO DADOS DE PARADAS DAS MÁQUINAS
        'paradas_maquina1': lista_paradas_maquina.count(1),                                         # 5.6.4.1 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 1
        'paradas_maquina3': lista_paradas_maquina.count(3),                                         # 5.6.4.2 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 3
        'paradas_maquina4': lista_paradas_maquina.count(4),                                         # 5.6.4.3 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 4
        'paradas_maquina5': lista_paradas_maquina.count(5),                                         # 5.6.4.4 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
        'paradas_maquina6': lista_paradas_maquina.count(6),                                         # 5.6.4.5 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 6
        'paradas_maquina7': lista_paradas_maquina.count(7),                                         # 5.6.4.6 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 7   
        #@MQMAQUINA3#
        #'paradas_maquina5': lista_paradas_maquina.count(id da máquina nova),                       # 5.6.4.7 - Variável que conta quantas paradas foram registradas no período filtrado na máquina com o ID 5
    
        'ultima_atualizacao': datetime.now()                                                        # 5.6.4.8 - Variável que pega a data e hora do último refresh na página.
    
    }

    return render(request, 'maquina.html', dados)
    