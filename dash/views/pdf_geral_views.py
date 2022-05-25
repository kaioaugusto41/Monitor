from django.shortcuts import get_object_or_404, render
from numpy import append
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .funcoes.consultas_banco import consultaProducao
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
        #p.rect(20, topo-750, 555, 500, fill=False)
        p.setFillGray(0.85)
        p.setStrokeGray(0.85)
        p.rect(20.7, topo-301, 553.7, 50.5, fill=True, stroke=False)
        p.setFillColor('black')
        p.setStrokeColor('black')
        p.setFontSize(13)
        p.drawCentredString(canto_direito/2, 570, 'Produção')
        p.line(20, 560, canto_direito-20, 560)
        p.drawString(140, 545, 'Máquina')
        p.line(300, 559, 300, 520)
        p.drawString(405, 545, 'Quantidade')

        #COMEÇO DA PRODUÇÃO DAS MÁQUINAS
        posicao_linha_hor = 540
        posicao_nome_maquina = 525
        posicao_linha_divisora = 540
        for i in range(8, 30):
            maquinas_filtradas.append(i)
        if maquinas_filtradas:
            fim_producao = topo-302-(len(maquinas_filtradas)*20)
            for i in maquinas_filtradas:
                if len(maquinas_filtradas) > 18:
                    if i == maquinas_filtradas[18]:
                        posicao_linha_hor = 820
                        posicao_nome_maquina = 805
                        posicao_linha_divisora = 820
                        p.showPage()
                p.line(20, posicao_linha_hor, canto_direito-20, posicao_linha_hor)
                p.drawString(30, posicao_nome_maquina, '{}'.format(Maquina.objects.get(id=i)))
                p.drawString(430, posicao_nome_maquina, '{}'.format(
                    consultaProducao(
                        dataInicial('GET', request, 'data_antiga_relatorio', 'hora_antiga'),
                        dataFinal('GET', request, 'data_nova_relatorio', 'hora_nova'), 
                        maquina_id=int(i)
                        )))
                if maquinas_filtradas.index(i) == len(maquinas_filtradas)-1:
                    p.line(300, posicao_linha_divisora-20, 300, 520)
                    p.rect(20, fim_producao, 555, 52+(len(maquinas_filtradas*20)), fill=False)
                    # n = range(0,50)
                    # for i in n:
                    #     if len(n) > 18:
                    #         if i == n[18]:
                    #             fim_producao = 820
                    #             p.showPage()
                    #     p.line(20, fim_producao-20, canto_direito-20, fim_producao-20)
                    #     fim_producao = fim_producao-20


                posicao_linha_hor = posicao_linha_hor-20
                posicao_nome_maquina = posicao_nome_maquina-20
                posicao_linha_divisora = posicao_linha_divisora - 20
        # Close the PDF object cleanly.
        p.showPage()
        p.save()

        # Get the value of the BytesIO buffer and write it to the response.
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)

        return response
