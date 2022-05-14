from django.contrib import admin
from .models import Maquina, Paradas_tipos, Producao

# Register your models here.
admin.site.register(Maquina)
admin.site.register(Producao)
admin.site.register(Paradas_tipos)

