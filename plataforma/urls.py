from django.urls import path
from . import views

urlpatterns = [
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dados_paciente/', views.dados_paciente_listar, name="dados_paciente"),
    path('dados_paciente/<str:id>/', views.dados_paciente, name="dadospaciente"),
]