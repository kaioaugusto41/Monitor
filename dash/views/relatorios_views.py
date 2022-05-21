from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse


# 6 - PÁGINA DE RELATÓRIOS
def relatorios(request):

    # 2.1 - LISTAS UTILIZADAS NA PÁGINA
    lista_producao_relatorio = []                                                                      # 2.1.1 - Lista que contem todos os registros de produção de todas as máquinas.
  
    # 4.1 - LISTA DE PARADAS POR MÁQUINA
    lista_paradas_maquina1 = []                                                                     # 4.1.1 - Contém todas as paradas da máquina 1
    lista_paradas_maquina3 = []                                                                     # 4.1.2 - Contém todas as paradas da máquina 3
    lista_paradas_maquina4 = []                                                                     # 4.1.4 - Contém todas as paradas da máquina 4
    lista_paradas_maquina5 = []                                                                     # 4.1.5 - Contém todas as paradas da máquina 5
    lista_paradas_maquina6 = []                                                                     # 4.1.6 - Contém todas as paradas da máquina 7
    lista_paradas_maquina7 = []                                                                     # 4.1.7 - Contém todas as paradas da máquina 7
    # @MQPARADAS1#
    # lista_paradas_maquina(id da máquina nova) = []                                                                   

    # 2.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                     # 2.5.1 - Se houver uma requisição do tipo POST na página...
        
        maquinas_filtradas = []                                                                     # 4.3.2 - Lista de máquinas com filtro...
        for maquina in Maquina.objects.values('id'):                                                # 4.3.3 - Loop que percorrerá todas as máquinas cadastradas no banco...
            maquina_filtrada = request.POST.get('filtro_{}'.format(maquina['id']), False)           # 4.3.3.1 - Bucando os valores filtrados no index.
            if maquina_filtrada != False:                                                           # 4.3.3.2 - Se o valor recebido for diferente de False...
                maquinas_filtradas.append(maquina_filtrada)                                         # 4.3.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)
        
        
        data_antiga_relatorio = request.POST.get('data_antiga_relatorio', False) + ' ' + request.POST.get('hora_antiga', False)   # 2.5.2 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_relatorio = request.POST.get('data_nova_relatorio', False) + ' ' + request.POST.get('hora_nova', False)         # 2.5.3 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                   # 2.5.4 - Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                 # 2.5.5 - Cursor que receberá os comandos SQL.
        
        # 2.5.6 - PRODUÇÃO DAS MÁQUINAS COM FILTRO
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_relatorio, data_nova_relatorio)) # 2.5.6.1 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        lista_producao_relatorio.clear()                                                               # 2.5.6.2 - Função que limpará a lista antes de adquirir dados novos.
        result = cursor.fetchall()                                                                   # 2.5.6.3 - Resultado da filtragem realizada anteriormente pelo usuário.
        lista_producao_relatorio.clear()                                                               # 2.5.6.4 - Função que limpará a lista antes de adquirir dados novos.
        for i in result:                                                                             # 2.5.6.5 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
            lista_producao_relatorio.append(i[0])                                                      # 2.5.6.5.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

        connection = sqlite3.connect('db.sqlite3')                                                  # 4.3.5 - Comando que realizada a conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 4.3.6 - Cursor que receberá todos os comandos que serão executados no banco de dados.
        cursor.execute("SELECT * FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_relatorio, data_nova_relatorio)) # 4.3.7 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        result = cursor.fetchall()                                                                  # 4.3.8 - Resultado obtido do banco de dados.
        lista_paradas_maquina1.clear()                                                              # 4.3.9 - Limpando a lista de paradas da máquina 1.
        lista_paradas_maquina3.clear()                                                              # 4.3.10 - Limpando a lista de paradas da máquina 3.
        lista_paradas_maquina4.clear()                                                              # 4.3.11 - Limpando a lista de paradas da máquina 4.
        lista_paradas_maquina5.clear()                                                              # 4.3.12 - Limpando a lista de paradas da máquina 5.
        lista_paradas_maquina6.clear()                                                              # 4.3.13 - Limpando a lista de paradas da máquina 6.
        lista_paradas_maquina7.clear()                                                              # 4.3.14 - Limpando a lista de paradas da máquina 7.
        # @MQPARADAS5#
        # lista_paradas_maquina(id).clear()
        for i in result:                                                                            # 4.3.15 - Loop que percorrerá todos os itens do resultado obtido na consulta realizada no banco de dados.
            if i[2] == 1:                                                                           # 4.3.15.1 - Se o terceiro item da lista percorrida for igual a 1...
                lista_paradas_maquina1.append(i[3])                                                 # 4.3.15.1.1 - Adiciona o item encontrado na lista de paradas da máquina 1.
            elif i[2] == 3:                                                                         # 4.3.15.2 - Se o terceiro item da lista percorrida for igual a 3...
                lista_paradas_maquina3.append(i[3])                                                 # 4.3.15.2.1 - Adiciona o item encontrado na lista de paradas da máquina 3.
            elif i[2] == 4:                                                                         # 4.3.15.3 - Se o terceiro item da lista percorrida for igual a 4...
                lista_paradas_maquina4.append(i[3])                                                 # 4.3.15.3.1 - Adiciona o tem encontrado na lista de paradas da máquina 4.
            elif i[2] == 5:                                                                         # 4.3.15.4 - Se o terceiro item da lista percorrida for igual a 5...
                lista_paradas_maquina5.append(i[3])                                                 # 4.3.15.4.1 - Adiciona o item encontrado na lista de paradas da máquina 5.
            elif i[2] == 6:                                                                         # 4.3.15.5 - Se o terceiro item da lista percorrida for igual a 6...
                lista_paradas_maquina6.append(i[3])                                                 # 4.3.15.5.1 - Adiciona o item encontrado na lista de paradas da máquina 6.
            elif i[2] == 7:                                                                         # 4.3.15.6 - Se o terceiro item da lista percorrida for igual a 7...
                lista_paradas_maquina7.append(i[3])                                                 # 4.3.15.6.1 - Adiciona o item encontrado na lista de paradas da máquina 7.
            # @MQPARADAS6#
            #  elif i[2] == (id):
                # lista_paradas_maquina(id).append(i[3])

        #maquinas_filtradas
        #data_antiga_relatorio
        #data_nova_relatorio
        #lista_producao_relatorio.count()
        #lista_paradas_maquina7
    
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
      
    }

    return render(request, 'relatorios.html', dados)