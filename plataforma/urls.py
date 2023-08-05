from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dadospaciente/', views.dados_paciente_listar, name="dadospaciente"),
    path('paciente/<str:id>/', views.dados_paciente, name="paciente"),
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso")
]