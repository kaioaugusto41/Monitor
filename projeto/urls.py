from email.mime import base
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from dash.api import viewset as dashviewset

route = routers.DefaultRouter()
route.register(r'maquina', dashviewset.maquinasViewSet, basename='maquina')
route.register(r'paradas', dashviewset.paradasViewSet, basename='paradas')
route.register(r'producao', dashviewset.producaoViewSet, basename='producao')
route.register(r'motivos_parada', dashviewset.motivosViewSet, basename='motivos_paradas')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('dash.urls')),
    path('api/', include(route.urls))
]
