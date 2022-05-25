from dash.models import Maquina

def renomeiaMaquina(request, name_input_nome_antigo, name_input_nome_novo):     
    nome_maquina_antigo = request.GET.get(name_input_nome_antigo, False)                         # 1.1.2 - Nome da máquina antes de ser renomeada.
    nome_maquina_novo = request.GET.get(name_input_nome_novo, False)                             # 1.1.3 - Nome da máquina após ser renomeada.
    maquina_a_renomear  = Maquina.objects.filter(nome_maquina=nome_maquina_antigo).update(nome_maquina=nome_maquina_novo)  # 1.1.4 - Comando para alterar o nome da máquina no banco de dados.