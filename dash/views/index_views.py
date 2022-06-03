# IMPORTAÇÕES DE BIBLIOTECAS E MÓDULOS
from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from dash.views.funcoes.filtra_maquinas import filtraMaquinas
from dash.views.funcoes.pega_datas import dataFinal, dataInicial
from .funcoes.renomeia_maquinas import renomeiaMaquina
from .funcoes.consultas_banco import adicionaParadasListas_, consultaProducao, adicionaProducaoLista
from .funcoes.ordenaLista import ordenaLista


# FUNÇÃO RESPONSÁVEL PELO BACKEND DA PÁGINA INDEX
def index(request):

    # 1 - Lista de paradas de cada máquina.
    lista_paradas_maquina1 = []                                                                     
    lista_paradas_maquina2 = []                                                                     
    lista_paradas_maquina3 = []                                                                     
    lista_paradas_maquina4 = []                                                                     
    lista_paradas_maquina5 = []                                                                     
    lista_paradas_maquina6 = []
    ####################################################                                                                     
    # @MQPARADAS1#                                     #
    # lista_paradas_maquina(id da máquina nova) = []   #                                                                
    ####################################################


    # 2 -  Funções responsáveis por ordenar as listas de paradas das máquinas.
    ordenaLista(lista_paradas_maquina1)
    ordenaLista(lista_paradas_maquina2)
    ordenaLista(lista_paradas_maquina3)
    ordenaLista(lista_paradas_maquina4)
    ordenaLista(lista_paradas_maquina5)
    ordenaLista(lista_paradas_maquina6)
    ####################################################                                                                     
    # @MQPARADAS1#                                     #
    # ordenaLista(lista_paradas_maquina(id da máq.))   #                                                                
    ####################################################


    # 3 - Quando houver uma requisição do tipo GET chama a função que renomeia a máquina. 
    if request.method == 'GET':                                                                     
        renomeiaMaquina(request, 'nome_maquina_antigo',  'nome_maquina_novo')
  

    # 4 - Lista de produção da página INDEX sem filtro de período.
    lista_producao_index = []                                                                       
    

    # 5 - Datas padrões ao carregar o site, sem filtro (00:00 do dia atual ao horário atual).
    data_antiga_index = str(datetime.now())[:11] + '00:00:01'                                       
    data_nova_index = str(datetime.now())[:19]


    # 6 - Função que adiciona a produção total no período das datas padrões na lista de produção do tópico #4.                                                     
    adicionaProducaoLista(data_antiga_index, data_nova_index, lista_producao_index)
    

    # 7 - Função que adiciona as paradas na lista de cada máquina no no tópico #1.
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina1, 1)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina2, 2)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina3, 3)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina4, 4)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina5, 5)
    adicionaParadasListas_(data_antiga_index, data_nova_index, lista_paradas_maquina6, 6)


    # 8 - Lista de máquinas a serem exibidas sem filtro.
    maquinas_filtradas = []                                                                         
    

    # 9 - Loop que percorre e adiciona todas os ids das máquinas do banco na lista do tópico #8
    for maquina in Maquina.objects.values('id'):                                                    
        maquinas_filtradas.append(maquina['id'])                                                    


    # 10 - Se houver uma requisição do tipo POST...
    if request.method == 'POST':

        # 11 - Lista de máquinas a serem exibidas com filtro.                                                                    
        maquinas_filtradas = []

        # 12 - Função que filtra as máquinas selecionadas no template.                                                                     
        filtraMaquinas('POST', request, maquinas_filtradas)

        # 13 - Função que adiciona a produção do período filtrado na lista de produção do tópico #4.
        adicionaProducaoLista(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_producao_index)
        
        # 14 - Função que adiciona as paradas do período filtrado nas listas de paradas do tópico #1.
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina1, 1)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina2, 2)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina3, 3)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina4, 4)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina5, 5)
        adicionaParadasListas_(dataInicial('POST', request, 'data_antiga_index', 'hora_antiga'), dataFinal('POST', request, 'data_nova_index', 'hora_nova'), lista_paradas_maquina6, 6)


    # 15 - Dados que serão exibidos no template, na página Index.html.
    dados = {

        # 16 - Variável: Todas as máquinas.
        'maquinas': Maquina.objects.all(),

        # 17 - Variável: Todos os tipos de paradas.
        'paradas_tipos': Paradas_tipos.objects.all(),
        
        # 18 - Variável: Máquinas com ou sem filtro.
        'maquinas_filtradas': Maquina.objects.filter(pk__in=maquinas_filtradas),  


        # 19 - Variáveis: Variável contendo a quantidade de repetição do id de cada máquina na lista de produção total.
        'producao_maquina1': lista_producao_index.count(1),                                         
        'producao_maquina2': lista_producao_index.count(2),                                         
        'producao_maquina3': lista_producao_index.count(3),                                         
        'producao_maquina4': lista_producao_index.count(4),                                         
        'producao_maquina5': lista_producao_index.count(5),                                         
        'producao_maquina6': lista_producao_index.count(6),
        ########################################################################                                              
        # @PMINDEX2#                                                           #
        #'producao_maquina8': lista_producao_index.count(id da máquina nova),  #                     
        ########################################################################


        # 20 - Variáveis: Variável contendo a quantidade de paradas em cada lista de paradas.
        'paradas_maquina1': len(lista_paradas_maquina1),                                            
        'paradas_maquina2': len(lista_paradas_maquina2),                                            
        'paradas_maquina3': len(lista_paradas_maquina3),                                            
        'paradas_maquina4': len(lista_paradas_maquina4),                                            
        'paradas_maquina5': len(lista_paradas_maquina5),                                            
        'paradas_maquina6': len(lista_paradas_maquina6),
        ######################################################                                            
        # @MQPARADAS7#                                       #
        #'paradas_maquina(id)': len(lista_paradas_maquina5), #   
        ######################################################


        # 21 - Variáveis: Variável contendo o número de repetições do ID de cada tipo de parada na lista de paradas da máquina 1.
        'parada_motivo1_maquina1': int(lista_paradas_maquina1.count(1)),                                 
        'parada_motivo2_maquina1': int(lista_paradas_maquina1.count(2)),                                 
        'parada_motivo3_maquina1': int(lista_paradas_maquina1.count(3)),                                 
        'parada_motivo4_maquina1': int(lista_paradas_maquina1.count(4)),                                 
        'parada_motivo5_maquina1': int(lista_paradas_maquina1.count(5)),


        # 22 - Variáveis: Variável contendo o número de repetições do ID de cada tipo de parada na lista de paradas da máquina 2.
        'parada_motivo1_maquina2': lista_paradas_maquina2.count(1),                                 
        'parada_motivo2_maquina2': lista_paradas_maquina2.count(2),                                 
        'parada_motivo3_maquina2': lista_paradas_maquina2.count(3),                                 
        'parada_motivo4_maquina2': lista_paradas_maquina2.count(4),                                 
        'parada_motivo5_maquina2': lista_paradas_maquina2.count(5),                                 


        # 23 - Variáveis: Variável contendo o número de repetições do ID de cada tipo de parada na lista de paradas da máquina 3.
        'parada_motivo1_maquina3': lista_paradas_maquina3.count(1),                                 
        'parada_motivo2_maquina3': lista_paradas_maquina3.count(2),                                 
        'parada_motivo3_maquina3': lista_paradas_maquina3.count(3),                                 
        'parada_motivo4_maquina3': lista_paradas_maquina3.count(4),                                 
        'parada_motivo5_maquina3': lista_paradas_maquina3.count(5),        


        # 24 - Variáveis: Variável contendo o número de repetições do ID de cada tipo de parada na lista de paradas da máquina 4.
        'parada_motivo1_maquina4': lista_paradas_maquina4.count(1),                                 
        'parada_motivo2_maquina4': lista_paradas_maquina4.count(2),                                 
        'parada_motivo3_maquina4': lista_paradas_maquina4.count(3),                                 
        'parada_motivo4_maquina4': lista_paradas_maquina4.count(4),                                 
        'parada_motivo5_maquina4': lista_paradas_maquina4.count(5),       


        # 25 - Variáveis: Variável contendo o número de repetições do ID de cada tipo de parada na lista de paradas da máquina 5.
        'parada_motivo1_maquina5': lista_paradas_maquina5.count(1),                                 
        'parada_motivo2_maquina5': lista_paradas_maquina5.count(2),                                 
        'parada_motivo3_maquina5': lista_paradas_maquina5.count(3),                                 
        'parada_motivo4_maquina5': lista_paradas_maquina5.count(4),                                 
        'parada_motivo5_maquina5': lista_paradas_maquina5.count(5),                                 

        # 26 - Variáveis: Variável contendo o número de repetições do ID de cada tipo de parada na lista de paradas da máquina 6.
        'parada_motivo1_maquina6': lista_paradas_maquina6.count(1),                                 
        'parada_motivo2_maquina6': lista_paradas_maquina6.count(2),                                 
        'parada_motivo3_maquina6': lista_paradas_maquina6.count(3),                                 
        'parada_motivo4_maquina6': lista_paradas_maquina6.count(4),                                 
        'parada_motivo5_maquina6': lista_paradas_maquina6.count(5),                                 

        # 27 - Variável: Contém a hora atual obtida pelo sistema operacional.
        'ultima_atualizacao': datetime.now()                                                        
 
    }

    # 28 - Retorna a renderição da página Index.html junto com os dados do tópico #15.
    return render(request, 'index.html', dados)                                                     
