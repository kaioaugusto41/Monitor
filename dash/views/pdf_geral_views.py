from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .funcoes.consultas_banco import consultaParadas, consultaProducao
from .funcoes.converte_data import converteData
from .funcoes.filtra_maquinas import filtraMaquinas
from .funcoes.pega_datas import dataInicial, dataFinal


def gera_pdf_geral(request):
    # 1.5 - PRODUÇÃO E PARADAS DAS MÁQUINAS COM FILTRO DE DATA E HORÁRIO (DEFINIDA PELO USUÁRIO)
    if request.method == 'GET':                                                                     # 1.5.1 - Se houver uma requisição do tipo POST na página...
   
        maquinas_filtradas = []                                                                     # 4.3.2 - Lista de máquinas com filtro...
        filtraMaquinas('GET', request, maquinas_filtradas)

        # Create the HttpResponse object with the appropriate PDF headers.
        response = HttpResponse(content_type='/pdf')
        response['Content-Disposition'] = 'attachment; filename="Relatório Geral.pdf"'

        buffer = BytesIO()

        # Create the PDF object, using the BytesIO object as its "file."
        p = canvas.Canvas(buffer)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        topo = 841.5
        canto_direito = 595
        meio_largura = 565/2
        meio_altura = 833/2

        # CABEÇALHO
        p.drawImage("logo.png", 233, topo-80, width=130, height=70)          # Logo
        p.setFontSize(12)
        p.rect(20, topo-55, 170, 20)
        p.drawString(25, topo-50, 'Emitido: {}'.format(converteData(str(datetime.now())[:16])))
        p.setFontSize(16)
        p.drawCentredString(canto_direito/2, 720, 'RELATÓRIO GERAL')

        # PERÍODO
        p.rect(20, topo-220, 555, 70, fill=False)
        p.setFillGray(0.85)
        p.setStrokeGray(0.85)
        p.rect(20.7, topo-201, 553.7, 50.5, fill=True, stroke=False)
        p.setFillColor('black')
        p.setStrokeColor('black')
        p.setFontSize(13)
        p.drawCentredString(canto_direito/2, 670, 'Período')
        p.line(20, 660, canto_direito-20, 660)
        p.line(20, 640, canto_direito-20, 640)
        p.drawString(140, 645, 'Data Inicial')
        p.drawString(110, 625, '{}'.format(converteData(dataInicial('GET', request, 'data_antiga_relatorio', 'hora_antiga'))))
        p.line(300, 660, 300, 620)
        p.drawString(405, 645, 'Data Final')
        p.drawString(375, 625, '{}'.format(converteData(dataFinal('GET', request, 'data_nova_relatorio', 'hora_nova'))))

        # PRODUÇÃO
        p.setFillGray(0.85)
        p.setStrokeGray(0.85)
        p.rect(20.7, topo-301, 553.7, 50.5, fill=True, stroke=False)
        p.setFillColor('black')
        p.setStrokeColor('black')
        p.setFontSize(13)
        # LINHA HORIZONTAL QUE FICA ACIMA DA STRING PRODUÇÃO
        p.line(20, 591, canto_direito-20, 591)
        # LINHA VERTICAL DO LADO ESQUERDO DA STRING PRODUÇÃO
        p.line(20, 591.5, 20, 540)
        p.drawCentredString(canto_direito/2, 570, 'Produção')
        # LINHA HORIZONTAL QUE FICA ABAIXO DA STRING PRODUÇÃO
        p.line(20, 560, canto_direito-20, 560)
        # LINHA VERTICAL DO LADO DIREITO DA STRING PRODUÇÃO
        p.line(canto_direito-20, 591.5, canto_direito-20, 540)
        # STRING MÁQUINA
        p.drawString(140, 545, 'Máquina')
        # LINHA VERTICAL DIVISORA QUE FICA ENTRE AS STRING MÁQUINA E QUANTIDADE
        p.line(300, 560, 300, 520)
        # STRING QUANTIDADE
        p.drawString(405, 545, 'Quantidade')

        

        # SE HOUVER MÁQUINAS NA LISTA DE MAQUINAS FILTRADAS...
        if maquinas_filtradas:

            #PRODUÇÃO DAS MÁQUINAS
            #___________________________________________________________________________________________________________________________________________________________
            inicio_producao = 540
            for i in maquinas_filtradas:
                # LINHA HORIZONTAL SUPERIOR
                p.line(20, inicio_producao, canto_direito-20, inicio_producao)
                # LINHA LATERAL VERTICAL - ESQUERDO
                p.line(20, inicio_producao, 20, inicio_producao-20)
                # STRING DO NOME DA MÁQUINA
                p.drawString(30, inicio_producao-15, '{}'.format((Maquina.objects.get(id=i))))
                # LINHA VERTICAL CENTRAL
                p.line(300, inicio_producao, 300, inicio_producao-20)
                # STRING DE PRODUÇÃO
                p.drawString(430, inicio_producao-15, '{}'.format(
                    consultaProducao(
                        dataInicial('GET', request, 'data_antiga_relatorio', 'hora_antiga'),
                        dataFinal('GET', request, 'data_nova_relatorio', 'hora_nova'), 
                        maquina_id=int(i)
                        )))
                # LINHA LATERAL VERTICAL - DIREITO
                p.line(canto_direito-20, inicio_producao, canto_direito-20, inicio_producao-20)
                if len(maquinas_filtradas) > 25:
                    if maquinas_filtradas.index(i) == 24:
                        # LINHA HORIZONTAL DO ÚLTIMO REGISTRO DA PRIMEIRA PÁGINA
                        p.line(20, inicio_producao-20, canto_direito-20, inicio_producao-20)

                # SE FOR O ÚLTIMO RESGISTRO, ADICIONE UMA LINHA ABAIXO....
                if maquinas_filtradas.index(i) == len(maquinas_filtradas)-1:
                    # LINHA HORIZONTAL INFERIOR
                    p.line(20, inicio_producao-20, canto_direito-20, inicio_producao-20)
                
                # IF A MEDIDA AO FINAL DA PRODUÇÃO FOR MENOR QUE 60MM...
                if inicio_producao < 60:
                    # ADICIONE UMA LINHA NO ÚLTIMO REGISTRO ANTES DE PULAR A PÁGINA
                    p.line(20, inicio_producao-20, canto_direito-20, inicio_producao-20)
                    # A PRODUÇÃO PERCORRERÁ A PARTIR DO TOPO DA PÁGINA NOVA
                    inicio_producao = topo
                    # ADICIONA UMA PÁGINA NOVA
                    p.showPage()

                # PARA CADA REGISTRO PULA 20MM
                inicio_producao = inicio_producao - 20
            
            # FIM DA PRODUÇÃO APÓS PERCORRER TODOS OS REGISTROS
            fim_producao = inicio_producao


            # INÍCIO PARADAS
            #___________________________________________________________________________________________________________________________________________________________
            def cabecalhoParadas(partida):
                p.setFillGray(0.85)
                p.setStrokeGray(0.85)
                p.rect(20.7, partida, 553.7, 50.5, fill=True, stroke=False)
                p.setFillColor('black')
                p.setStrokeColor('black')
                p.setFontSize(13)
                # LINHA HORIZONTAL QUE FICA ACIMA DA STRING PARADAS
                p.line(20, partida+51, canto_direito-20, partida+51)
                # LINHA VERTICAL DO LADO ESQUERDO DA STRING PARADAS
                p.line(20, partida+51, 20, partida)
                # STRING DE PARADAS
                p.drawCentredString(canto_direito/2, partida+30, 'Paradas')
                # LINHA HORIZONTAL QUE FICA ABAIXO DA STRING PARADAS
                p.line(20, partida+20, canto_direito-20, partida+20)
                # LINHA VERTICAL DO LADO DIREITO DA STRING PARADAS
                p.line(canto_direito-20, partida+51, canto_direito-20, partida)
                # STRING DA MÁQUINA
                p.drawString(140, partida+5, 'Máquina')
                # LINHA VERTICAL DIVISÓRIA QUE FICA ENTRE AS DUAS STRINGS MÁQUINA E QUANTIDADE
                p.line(300, partida+20, 300, partida)
                # STRING DA QUANTIDADE
                p.drawString(405, partida+5, 'Quantidade')

            # VARIÁVEL DO INÍCIO DAS PARADAS 
            inicio_paradas = fim_producao-100

            # SE O FIM DA PRODUÇÃO DEIXAR UM ESPAÇO RESTANTE DE 120MM...
            if fim_producao > 120:
                # O INÍCIO DAS PARADAS ACONTECERÁ A PARTIR DO FIM DA PRODUÇÃO
                cabecalhoParadas(inicio_paradas)
                for i in maquinas_filtradas:
                    # LINHA HORIZONTAL SUPERIOR
                    p.line(20, inicio_paradas, canto_direito-20, inicio_paradas)
                    # LINHA LATERAL VERTICAL - ESQUERDO
                    p.line(20, inicio_paradas, 20, inicio_paradas-20)
                    # STRING DO NOME DA MÁQUINA
                    p.drawString(30, inicio_paradas-15, '{}'.format((Maquina.objects.get(id=i))))
                    # LINHA VERTICAL CENTRAL
                    p.line(300, inicio_paradas, 300, inicio_paradas-20)
                    # STRING DE PRODUÇÃO
                    p.drawString(430, inicio_paradas-15, '{}'.format(
                        consultaParadas(
                            dataInicial('GET', request, 'data_antiga_relatorio', 'hora_antiga'),
                            dataFinal('GET', request, 'data_nova_relatorio', 'hora_nova'), 
                            maquina_id=int(i)
                            )))
                    # LINHA LATERAL VERTICAL - DIREITO
                    p.line(canto_direito-20, inicio_paradas, canto_direito-20, inicio_paradas-20)
                    # SE FOR O ÚLTIMO REGISTRO...
                    if maquinas_filtradas.index(i) == len(maquinas_filtradas)-1:
                        # ADICIONA UMA LINHA HORIZONTAL ABAIXO DO ÚLTIMO REGISTRO
                        p.line(20, inicio_paradas-20, canto_direito-20, inicio_paradas-20)
                    
                    # SE O INÍCIO DAS PARADAS APÓS PERCORRER FOR MENOR QUE 60MM...
                    if inicio_paradas < 60:
                        # ADICIONA UMA LINHA ABAIXO DO ÚLTIMO REGISTRO ANTES DE PULAR A PÁGINA
                        p.line(20, inicio_paradas-20, canto_direito-20, inicio_paradas-20)
                        # O INÍCIO APÓS PULAR A PÁGINA SERÁ NO TOPO DA PÁGINA
                        inicio_paradas = topo
                        # ADICIONA UMA PÁGINA NOVA
                        p.showPage()

                    # PARA CADA REGISTRO PERCORRIDO PULA 20MM
                    inicio_paradas = inicio_paradas - 20
            
            # SE O ESPAÇO DEIXADO PELA PRODUÇÃO FOR MENOR QUE 120MM...
            else:
                # ADICIONA UMA PÁGINA NOVA
                p.showPage()
                # O INÍCIO DAS PARADAS SERÁ NO TOPO DA PÁGINA MENOS 100MM
                inicio_paradas = topo-100
                # CABEÇALHO DAS PARADAS
                cabecalhoParadas(inicio_paradas)
                for i in maquinas_filtradas:
                    # LINHA HORIZONTAL SUPERIOR
                    p.line(20, inicio_paradas, canto_direito-20, inicio_paradas)
                    # LINHA LATERAL VERTICAL - ESQUERDO
                    p.line(20, inicio_paradas, 20, inicio_paradas-20)
                    # STRING DO NOME DA MÁQUINA
                    p.drawString(30, inicio_paradas-15, '{}'.format((Maquina.objects.get(id=i))))
                    # LINHA VERTICAL CENTRAL
                    p.line(300, inicio_paradas, 300, inicio_paradas-20)
                    # STRING DE PRODUÇÃO
                    p.drawString(430, inicio_paradas-15, '{}'.format(
                        consultaParadas(
                            dataInicial('GET', request, 'data_antiga_relatorio', 'hora_antiga'),
                            dataFinal('GET', request, 'data_nova_relatorio', 'hora_nova'), 
                            maquina_id=int(i)
                            )))
                    # LINHA LATERAL VERTICAL - DIREITO
                    p.line(canto_direito-20, inicio_paradas, canto_direito-20, inicio_paradas-20)
                    # SE FOR O ÚLTIMO REGISTRO...
                    if maquinas_filtradas.index(i) == len(maquinas_filtradas)-1:
                        # ADICIONA UMA LINHA HORIZONTAL ABAIXO DO ÚLTIMO REGISTRO
                        p.line(20, inicio_paradas-20, canto_direito-20, inicio_paradas-20)
                    # SE O INÍCIO DAS PARADAS APÓS PERCORRER FOR MENOR QUE 60MM...
                    if inicio_paradas < 60:
                        # ADICIONA UMA LINHA ABAIXO DO ÚLTIMO REGISTRO ANTES DE PULAR DE PÁGINA
                        p.line(20, inicio_paradas-20, canto_direito-20, inicio_paradas-20)
                        # O INÍCIO DAS PARADAS APÓS PULAR A PÁGINA SERÁ A PARTIR DO TOPO
                        inicio_paradas = topo
                        # ADICIONA UMA NOVA PÁGINAS
                        p.showPage()

                    # PARA CADA REGISTRO PERCORRIDO PULA 20MM
                    inicio_paradas = inicio_paradas - 20


        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response
