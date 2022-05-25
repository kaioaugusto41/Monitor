from dash.models import Maquina

def filtraMaquinas(metodo, request, lista_maquinas_filtradas):
    metodo = metodo
    for maquina in Maquina.objects.values('id'):                                                # 4.3.3 - Loop que percorrerá todas as máquinas cadastradas no banco...
        if metodo == 'POST':
            maquina_filtrada = request.POST.get('filtro_{}'.format(maquina['id']), False)           # 4.3.3.1 - Bucando os valores filtrados no index.
        elif metodo == 'GET':
            maquina_filtrada = request.GET.get('filtro_{}'.format(maquina['id']), False)
        if maquina_filtrada != False:                                                           # 4.3.3.2 - Se o valor recebido for diferente de False...
            lista_maquinas_filtradas.append(maquina_filtrada)                                         # 4.3.3.2.1 - Adicionando os ids a serem mostrados na lista (maquinas_filtradas)