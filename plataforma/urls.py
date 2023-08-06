
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path
from . import views

urlpatterns = [
    path('', views.pacientes, name='pacientes'),
    path('pacientes/', views.pacientes, name='pacientes'),
    path('dadospaciente/', views.dados_paciente_listar, name="dadospaciente"),
    path('paciente/<str:id>/', views.dados_paciente, name="paciente"),
    path('grafico_peso/<str:id>/', views.grafico_peso, name="grafico_peso"),
    path('plano_alimentar_listar/', views.plano_alimentar_listar, name="plano_alimentar_listar"),
    path('plano_alimentar/<str:id>/', views.plano_alimentar, name="plano_alimentar"),
    path('refeicao/<str:id_paciente>/', views.refeicao, name="refeicao"),
    path('opcao/<str:id_paciente>/', views.opcao, name="opcao"),
    path('gerarpdf/<str:id_paciente>/', views.pdf, name="pdf"),
    path('logout/', views.logout, name="sair"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)