from dash.models import Maquina

def dataInicial(metodo, request, name_input_data, name_input_hora):
    metodo = metodo
             
    if metodo == 'POST':
        data_inicial = request.POST.get(name_input_data, False) + ' ' + request.POST.get(name_input_hora, False)
    elif metodo == 'GET':
        data_inicial = request.GET.get(name_input_data, False) + ' ' + request.GET.get(name_input_hora, False)
    return data_inicial

def dataFinal(metodo, request, name_input_data, name_input_hora):
    metodo = metodo
    if metodo == 'POST':
        data_final = request.POST.get(name_input_data, False) + ' ' + request.POST.get(name_input_hora, False)         
    elif metodo == 'GET':
        data_final = request.GET.get(name_input_data, False) + ' ' + request.GET.get(name_input_hora, False)
    return data_final        