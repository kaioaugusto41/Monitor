from rest_framework import viewsets
from dash.api import serializers
from dash import models

class maquinasViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.maquinasSerializer
    queryset = models.Maquina.objects.all()

class paradasViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.paradasSerializer
    queryset = models.Paradas.objects.all()

class producaoViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.producaoSerializer
    queryset = models.Producao.objects.all()

class motivosViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.motivosSerializer
    queryset = models.Paradas_tipos.objects.all()