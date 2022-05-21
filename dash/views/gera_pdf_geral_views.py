from django.shortcuts import get_object_or_404, render
from dash.models import Maquina, Paradas_tipos
from datetime import datetime
import sqlite3
from io import BytesIO
from reportlab.pdfgen import canvas
from django.http import HttpResponse



def gera_pdf_geral(request):
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


    p.drawImage("logo.png", 0, 710, width=130, height=130)          # Logo
    p.setFontSize(12)
    p.rect(canto_direito-220, topo-95, 200, 60)
    p.drawString(canto_direito-210, topo-50, 'Emitido: 13/05/2022 às 11:45')
    p.drawString(canto_direito-210, topo-70, 'Data inicial: 26/04/2022 às 09:48')
    p.drawString(canto_direito-210, topo-90, 'Data final: 13/05/2022 às 11:45')
    p.setFontSize(16)
    p.drawCentredString(canto_direito/2, 700, 'RELATÓRIO GERAL')
    p.line(20, topo-160, canto_direito-20, topo-160)                # Linha horizontal superior
    p.line(20, 20, canto_direito-20, 20)                            # Linha horizontal inferior
    #p.line(20, topo-160, 20, 20)                                    # Linha vertical esquerda
    #p.line(canto_direito-20, topo-160, canto_direito-20, 20)        # Linha vertical direita
    p.rect(20, topo-250, 555, 60)

    # Close the PDF object cleanly.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    if request.method == 'GET':
        print('**********************************')
    return response
