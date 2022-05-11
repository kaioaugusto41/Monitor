from tkinter import CASCADE
from django.db import models

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