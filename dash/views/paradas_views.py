from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse



# 4 - PÁGINA PARADAS (MENÚ)
def paradas(request):

    # 4.1 - LISTA DE PARADAS POR MÁQUINA
    lista_paradas_maquina1 = []                                                                     # 4.1.1 - Contém todas as paradas da máquina 1
    lista_paradas_maquina3 = []                                                                     # 4.1.2 - Contém todas as paradas da máquina 3
    lista_paradas_maquina4 = []                                                                     # 4.1.4 - Contém todas as paradas da máquina 4
    lista_paradas_maquina5 = []                                                                     # 4.1.5 - Contém todas as paradas da máquina 5
    lista_paradas_maquina6 = []                                                                     # 4.1.6 - Contém todas as paradas da máquina 7
    lista_paradas_maquina7 = []                                                                     # 4.1.7 - Contém todas as paradas da máquina 7
    # @MQPARADAS1#
    # lista_paradas_maquina(id da máquina nova) = []                                                                   

    if len(lista_paradas_maquina1) > 0:                                                             # 4.1.8 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina1 = lista_paradas_maquina1.sort()                                      # 4.1.8.1 - Ordenando a lista.
    if len(lista_paradas_maquina3) > 0:                                                             # 4.1.9 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina3 = lista_paradas_maquina3.sort()                                      # 4.1.9.1 - Ordenando a lista.
    if len(lista_paradas_maquina4) > 0:                                                             # 4.1.10 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina4 = lista_paradas_maquina4.sort()                                      # 4.1.10.1 - Ordenando a lista.
    if len(lista_paradas_maquina5) > 0:                                                             # 4.1.11 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina5 = lista_paradas_maquina5.sort()                                      # 4.1.11.1 - Ordenando a lista.
    if len(lista_paradas_maquina6) > 0:                                                             # 4.1.12 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina6 = lista_paradas_maquina6.sort()                                      # 4.1.12.1 - Ordenando a lista.
    if len(lista_paradas_maquina7) > 0:                                                             # 4.1.13 - Se a quantidade de itens na lista 'lista_paradas_maquina1' for maior que zero.
        lista_paradas_maquina7 = lista_paradas_maquina7.sort()                                      # 4.1.13.1 - Ordenando a lista.
    # @MQPARADAS2#
    # if len(lista_paradas_maquina(id)) > 0:
        # lista_paradas_maquina(id) = lista_paradas_maquina(id).sort()

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
    lista_paradas_maquina6.clear()                                                                  # 4.2.12 - Limpando a lista de paradas da máquina 6.
    lista_paradas_maquina7.clear()                                                                  # 4.2.13 - Limpando a lista de paradas da máquina 7.
    # @MQPARADAS3#
    # lista_paradas_maquina(id).clear()
    for i in result:                                                                                # 4.2.14 - Loop que percorrerá todos os itens do resultado obtido na consulta realizada no banco de dados.
        if i[2] == 1:                                                                               # 4.2.14.1 - Se o terceiro item da lista percorrida for igual a 1...
            lista_paradas_maquina1.append(i[3])                                                     # 4.2.14.1.1 - Adiciona o item encontrado na lista de paradas da máquina 1.
        elif i[2] == 3:                                                                             # 4.2.14.2 - Se o terceiro item da lista percorrida for igual a 3...
            lista_paradas_maquina3.append(i[3])                                                     # 4.2.14.2.1 - Adiciona o item encontrado na lista de paradas da máquina 3.
        elif i[2] == 4:                                                                             # 4.2.14.3 - Se o terceiro item da lista percorrida for igual a 4...
            lista_paradas_maquina4.append(i[3])                                                     # 4.2.14.3.1 - Adiciona o tem encontrado na lista de paradas da máquina 4.
        elif i[2] == 5:                                                                             # 4.2.14.4 - Se o terceiro item da lista percorrida for igual a 5...
            lista_paradas_maquina5.append(i[3])                                                     # 4.2.14.4.1 - Adiciona o item encontrado na lista de paradas da máquina 5.
        elif i[2] == 6:                                                                             # 4.2.14.5 - Se o terceiro item da lista percorrida for igual a 6...
            lista_paradas_maquina6.append(i[3])                                                     # 4.2.14.5.1 - Adiciona o item encontrado na lista de paradas da máquina 6.
        elif i[2] == 7:                                                                             # 4.2.14.6 - Se o terceiro item da lista percorrida for igual a 7...
            lista_paradas_maquina7.append(i[3])                                                     # 4.2.14.6.1 - Adiciona o item encontrado na lista de paradas da máquina 7.
        # @MQPARADAS4#
            # elif i[2] == (id):
            # lista_paradas_maquina(id).append(i[3])
    
    maquinas_filtradas = []                                                                         # 4.2.15 - Lista de ids das máquinas a serem exibidas na página Paradas (Sem filtro).
    for maquina in Maquina.objects.values('id'):                                                    # 4.2.16 - Loop que percorrerá todas as máquinas cadastradas no banco...
        maquinas_filtradas.append(maquina['id'])                                                    # 4.2.16.1 - Adicionando cada máquina cadastrada percorrida na lista acima (maquinas_filtradas)
    
    # 4.3 - PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':                                                                    # 4.3.1 - Se houver uma requisição do tipo POST na página...
        
        maquinas_filtradas = []                                                                     # 4.3.2 - Lista de máquinas com filtro...
        for maquina in Maquina.objects.values('id'):                                                # 4.3.3 - Loop que percorrerá todas as máquinas cadastradas no banco...
            maquina_filtrada = request.POST.get('filtro_{}'.format(maquina['id']), False)           # 4.3.3.1 - Bucando os valores filtrados no index.
            if maquina_filtrada != False:                                                           # 4.3.3.2 - Se o valor recebido for diferente de False...
                maquinas_filtradas.append(maquina_filtrada)                                         # 4.3.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)
        
        data_antiga_paradas = request.POST.get('data_antiga_paradas', False) + ' ' + request.POST.get('hora_antiga', False)     # 4.3.3 - Data inicial definida pelo usuário (Início do filtro).
        data_nova_paradas = request.POST.get('data_nova_paradas', False) + ' ' + request.POST.get('hora_nova', False)           # 4.3.4 - Data final definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                                  # 4.3.5 - Comando que realizada a conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                                # 4.3.6 - Cursor que receberá todos os comandos que serão executados no banco de dados.
        cursor.execute("SELECT * FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga_paradas, data_nova_paradas)) # 4.3.7 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
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
    
    # 4.4 - DADOS QUE SERÃO JOGADOS PARA O TEMPLATE
    dados = {
        
        'maquinas': Maquina.objects.all(),                                                          
        
        # MÁQUINAS QUE SERÃO MOSTRADAS COM FILTRO (AS QUE O USUÁRIO SELECIONAR APENAS)
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),                    # 3.4.1 - Comando que busca todas as máquinas cadastradas no banco.

        
        'ultima_atualizacao': datetime.now(),                                                       # 4.4.2 - Variável que conterá a data do último refresh da página.
        'paradas_tipos': Paradas_tipos.objects.all(),                                               # 4.4.3 - Variável que conterá todos os motivos de paradas cadastrados no banco de dados.

        # 4.4.1 - INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'paradas_maquina1': len(lista_paradas_maquina1),                                            # 4.4.1.1 - Variável que conterá a quantidade de paradas da máquina 1.
        'paradas_maquina3': len(lista_paradas_maquina3),                                            # 4.4.1.2 - Variável que conterá a quantidade de paradas da máquina 3.
        'paradas_maquina4': len(lista_paradas_maquina4),                                            # 4.4.1.3 - Variável que conterá a quantidade de paradas da máquina 4.
        'paradas_maquina5': len(lista_paradas_maquina5),                                            # 4.4.1.4 - Variável que conterá a quantidade de paradas da máquina 5.
        'paradas_maquina6': len(lista_paradas_maquina6),                                            # 4.4.1.5 - Variável que conterá a quantidade de paradas da máquina 6.
        'paradas_maquina7': len(lista_paradas_maquina7),                                            # 4.4.1.6 - Variável que conterá a quantidade de paradas da máquina 7.
        # @MQPARADAS7#
        #'paradas_maquina(id)': len(lista_paradas_maquina5),

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

        # 4.4.6 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 6
        'parada_motivo1_maquina6': lista_paradas_maquina6.count(1),                                 # 4.4.6.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 6.
        'parada_motivo2_maquina6': lista_paradas_maquina6.count(2),                                 # 4.4.6.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 6.
        'parada_motivo3_maquina6': lista_paradas_maquina6.count(3),                                 # 4.4.6.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 6.
        'parada_motivo4_maquina6': lista_paradas_maquina6.count(4),                                 # 4.4.6.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 6.
        'parada_motivo5_maquina6': lista_paradas_maquina6.count(5),                                 # 4.4.6.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 6.

        # 4.4.6 - INÍCIO DOS MOTIVOS DE PARADAS MÁQUINA 7
        'parada_motivo1_maquina7': lista_paradas_maquina7.count(1),                                 # 4.4.7.1 - Variável que conterá a quantidade de paradas do motivo 1 na máquina 7.
        'parada_motivo2_maquina7': lista_paradas_maquina7.count(2),                                 # 4.4.7.2 - Variável que conterá a quantidade de paradas do motivo 2 na máquina 7.
        'parada_motivo3_maquina7': lista_paradas_maquina7.count(3),                                 # 4.4.7.3 - Variável que conterá a quantidade de paradas do motivo 3 na máquina 7.
        'parada_motivo4_maquina7': lista_paradas_maquina7.count(4),                                 # 4.4.7.4 - Variável que conterá a quantidade de paradas do motivo 4 na máquina 7.
        'parada_motivo5_maquina7': lista_paradas_maquina7.count(5),                                 # 4.4.7.5 - Variável que conterá a quantidade de paradas do motivo 5 na máquina 7.
        
        # @MQPARADAS8#
        #'parada_motivo1_maquina(id)': lista_paradas_maquina(id).count(1),
        #'parada_motivo2_maquina(id)': lista_paradas_maquina(id).count(2),
        #'parada_motivo3_maquina(id)': lista_paradas_maquina(id).count(3),
        #'parada_motivo4_maquina(id)': lista_paradas_maquina(id).count(4),
        #'parada_motivo5_maquina(id)': lista_paradas_maquina(id).count(5),
    }

    return render(request, 'paradas.html', dados)                                                   # 4.5 - Função que renderiza a página paradas.html com os dados referenciados anteriormente.

