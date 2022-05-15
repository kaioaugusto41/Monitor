from dataclasses import field
from rest_framework import serializers
from dash import models

class maquinasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Maquina
        fields = '__all__'

class paradasSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paradas
        fields = '__all__'

class producaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Producao
        fields = '__all__'

class motivosSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Paradas_tipos
        fields = '__all__'