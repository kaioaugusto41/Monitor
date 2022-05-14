from pyexpat import model
from tkinter import CASCADE
from django.db import models
from datetime import datetime

class Maquina(models.Model):
    nome_maquina = models.CharField(max_length=200, blank=False)
    status_maquina = models.BooleanField(default=False)
    def __str__(self):
       return self.nome_maquina

class Producao(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    nome_produto = models.CharField(max_length=200)
    quantidade= models.IntegerField(default=1, blank=True)
    horario_producao = models.DateTimeField()

    def __str__(self):
        return self.nome_produto

class Paradas_tipos(models.Model):
    titulo_parada = models.CharField(max_length=300)
    descricao_parada = models.TextField()

    def __str__(self):
        return self.titulo_parada

class Paradas(models.Model):
    parada_tipo = models.ForeignKey(Paradas_tipos, on_delete=models.CASCADE)
    maquina_parada = models.ForeignKey(Maquina, on_delete=models.CASCADE)
    horario_parada = models.DateTimeField()

    def __str__(self):
        return self.parada_tipo