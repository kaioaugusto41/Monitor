import sqlite3

def consultaProducao(data_inicial, data_final, maquina_id):
    lista_producao = []
    connection = sqlite3.connect('db.sqlite3')                                                      # 1.1.4 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 1.1.5 - Cursor que receberá os comandos do banco de dados.
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_inicial, data_final)) # 1.1.6 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 1.1.7 - Resultado da filtragem padrão.
    lista_producao.clear()                                                                 # 1.1.8 - Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                                # 1.1.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao.append(i[0])                                                        # 1.1.9.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

    return lista_producao.count(maquina_id)

def adicionaProducaoLista(data_inicial, data_final, lista_producao):
    connection = sqlite3.connect('db.sqlite3')                                                      # 1.1.4 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 1.1.5 - Cursor que receberá os comandos do banco de dados.
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_inicial, data_final)) # 1.1.6 - Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 1.1.7 - Resultado da filtragem padrão.
    lista_producao.clear()                                                                 # 1.1.8 - Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                                # 1.1.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_producao.append(i[0])                                                        # 1.1.9.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

def consultaParadas(data_inicial, data_final, maquina_id):
    lista_paradas = []
    connection = sqlite3.connect('db.sqlite3')                                                      # 1.1.4 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 1.1.5 - Cursor que receberá os comandos do banco de dados.
    cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_inicial, data_final)) # 1.5.7.1 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 1.1.7 - Resultado da filtragem padrão.
    lista_paradas.clear()                                                                 # 1.1.8 - Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                                # 1.1.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_paradas.append(i[0])          

    return lista_paradas.count(maquina_id)

def adicionaParadasLista(data_inicial, data_final, lista_paradas):
    connection = sqlite3.connect('db.sqlite3')                                                      # 1.1.4 - Função que realiza a conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                                    # 1.1.5 - Cursor que receberá os comandos do banco de dados.
    cursor.execute("SELECT maquina_parada_id FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_inicial, data_final)) # 1.5.7.1 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 1.1.7 - Resultado da filtragem padrão.
    lista_paradas.clear()                                                                 # 1.1.8 - Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                                # 1.1.9 - Loop que percorrerá os dados de produção e adicionará na lista de produção.
        lista_paradas.append(i[0])                                                        # 1.1.9.1 - Função que adicionará na lista de produção geral o primeiro item da lista retornada do banco.

def adicionaParadasListas_(data_antiga, data_nova, lista_paradas_maquina, id):
    connection = sqlite3.connect('db.sqlite3')                                                      # 1.2.4 - Função que realiza a conexão com o banco Sqlite.
    cursor = connection.cursor()                                                                    # 1.2.5 - Cursor que receberá todos os comandos que serão executados no banco de dados.
    cursor.execute("SELECT * FROM dash_paradas WHERE horario_parada BETWEEN '{}' AND '{}'".format(data_antiga, data_nova)) # 1.2.6 - Cursor com o comando que filtrará as paradas de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                                      # 1.2.7 - Resultado obtido da consulta realizada no banco.
    lista_paradas_maquina.clear()                                                                  # 1.2.8 - Limpando a lista de paradas da máquina 1.    
    for i in result:                                                                                # 1.2.14 - Loop que percorrerá todos os itens do resultado obtido na consulta realizada no banco de dados.
        if i[2] == id:                                                                               # 1.2.14.1 - Se o terceiro item da lista percorrida for igual a 1...
            lista_paradas_maquina.append(i[3])                                                     # 1.2.14.1.1 - Adiciona o item encontrado na lista de paradas da máquina 1.
 