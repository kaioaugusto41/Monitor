from django.shortcuts import render
from .models import Maquina
from datetime import datetime
import sqlite3

def index(request):
    # VARIÁVEIS

    # REQUISIÇÃO DA EDIÇÃO DOS NOMES DAS MÁQUINAS 
    if request.method == 'GET':
        nome_maquina_antigo = request.GET.get('nome_maquina_antigo', False)             # Nome da máquina antes de ser renomeada.
        nome_maquina_novo = request.GET.get('nome_maquina_novo', False)                 # Nome da máquina após ser renomeada.
        maquina_a_renomear  = Maquina.objects.filter(nome_maquina=nome_maquina_antigo).update(nome_maquina=nome_maquina_novo)  #Comando para alterar o nome da máquina no banco de dados.
  

    # PRODUÇÃO DAS MÁQUINAS SEM FILTRO (PADRÃO)
    lista_producao_index = []                                                           # Lista que contém todas as produções de todas as máquinas.
    data_antiga_index = str(datetime.now())[:11] + '00:00:01'                           # Data antiga sem filtro.
    data_nova_index = str(datetime.now())[:19]                                          # Data atual sem filtro.
    connection = sqlite3.connect('db.sqlite3')                                          # Comando de conexão com o banco de dados Sqlite.
    cursor = connection.cursor()                                                        # Cursor que receberá os comandos SQL.
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_index, data_nova_index))  # Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (meia noite do dia atual) ao dia e horário atual.
    result = cursor.fetchall()                                                          # Resultado da filtragem padrão.
    lista_producao_index.clear()                                                        # Função que limpará a lista antes de adquirir dados novos.
    for i in result:                                                                    # Loop que percorrerá os dados de produção e adicionará na lista de produção da página index.
        lista_producao_index.append(i[0])

    # FILTRO DE DADOS POR DATA (DEFINIDA PELO USUÁRIO)
    if request.method == 'POST':
        data_antiga_index = request.POST.get('data_antiga_index', False) + ' ' + request.POST.get('hora_antiga', False)     # Data antiga definida pelo usuário (Início do filtro).
        data_nova_index = request.POST.get('data_nova_index', False) + ' ' + request.POST.get('hora_nova', False)           # Data nova definida pelo usuário (Final do filtro).
        connection = sqlite3.connect('db.sqlite3')                                      # Comando de conexão com o banco de dados Sqlite.
        cursor = connection.cursor()                                                    # Cursor que receberá os comandos SQL.
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_index, data_nova_index)) # Cursor com o comando que filtrará a produção de todas as máquinas da data_antiga (Data início definida pelo usuário) até a data_nova (Data final definida pelo usuário).
        result = cursor.fetchall()                                                      # Resultado da filtragem realizada anteriormente pelo usuário.
        lista_producao_index.clear()                                                    # Função que limpará a lista antes de adquirir dados novos.
        for i in result:                                                                # Loop que percorrerá os dados de produção e adicionará na lista de produção da página index.
            lista_producao_index.append(i[0])

    
    dados = {
        'maquinas': Maquina.objects.all(),                                              # Comando que busca todas as máquinas cadastradas no banco.

        #INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA INDEX
        'producao_maquina1': lista_producao_index.count(1),                             # Conta quantas peças foram produzidas no período filtrado na máquina com o ID 1
        'producao_maquina3': lista_producao_index.count(3),                             # Conta quantas peças foram produzidas no período filtrado na máquina com o ID 3
        'producao_maquina4': lista_producao_index.count(4),                             # Conta quantas peças foram produzidas no período filtrado na máquina com o ID 4
        'producao_maquina5': lista_producao_index.count(5),                             # Conta quantas peças foram produzidas no período filtrado na máquina com o ID 5

        'ultima_atualizacao': datetime.now()                                            # Função que pega a data e o horário atual para indicar a última atualização.
 
    }

    return render(request, 'index.html', dados)                                         # Função que renderiza a página index.html com os dados referenciado anteriormente.


def geral(request):
    dados = {
        # INÍCIO DAS MÁQUINAS NA PÁGINA GERAL
        'maquina1': Maquina.objects.get(id=1),
        'maquina3': Maquina.objects.get(id=3),
        'maquina4': Maquina.objects.get(id=4),
        'maquina5': Maquina.objects.get(id=5)
    }

    return render(request, 'geral.html', dados)

def producao(request):
    
    lista_producao_producao = [] # CONTÉM A PRODUÇÃO DE TODAS AS MÁQUINAS

    # PRODUÇÃO DAS MÁQUINAS SEM FILTRO
    lista_producao_producao = []       # CONTÉM A PRODUÇÃO DE TODAS AS MÁQUINAS
    data_antiga_producao = str(datetime.now())[:11] + '00:00:01'   # Data antiga sem filtro
    data_nova_producao = str(datetime.now()) [:19]                      # Data nova sem filtro
    connection = sqlite3.connect('db.sqlite3')
    cursor = connection.cursor()
    cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_producao, data_nova_producao))
    result = cursor.fetchall()
    for i in result:
        lista_producao_producao.append(i[0])
    
    if request.method == 'POST':
        data_antiga_producao = request.POST.get('data_antiga_producao', False) + ' ' + request.POST.get('hora_antiga', False) 
        data_nova_producao = request.POST.get('data_nova_producao', False) + ' ' + request.POST.get('hora_nova', False)
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()
        cursor.execute("SELECT maquina_id FROM dash_producao WHERE horario_producao BETWEEN '{}' AND '{}'".format(data_antiga_producao, data_nova_producao))
        result = cursor.fetchall()
        for i in result:
            lista_producao_producao.append(i[0])
        print(data_antiga_producao, data_nova_producao)
    dados = {
        'maquinas': Maquina.objects.all(),

        # INÍCIO DADOS DE PRODUÇÃO DAS MÁQUINAS NA PÁGINA PRODUÇÃO
        'producao_maquina1': lista_producao_producao.count(1),
        'producao_maquina3': lista_producao_producao.count(3),
        'producao_maquina4': lista_producao_producao.count(4),
        'producao_maquina5': lista_producao_producao.count(5),

        'data_antiga': data_antiga_producao,
        'data_nova': data_nova_producao,

        'ultima_atualizacao': datetime.now()
    }
    return render(request, 'producao.html', dados)


