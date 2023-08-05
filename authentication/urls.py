
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.conf import settings
from django.views.static import serve
from django.urls import path
from . import views

urlpatterns = [
   
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logar/', views.logar, name='logar'),
    path('sair/', views.sair, name="sair"),
    path('ativar_conta/<str:token>/', views.ativar_conta, name="ativar_conta"), #url para ativar a conta do usuario
    #re_path(r'^media/(?P<path>.*)$',serve, {'document_root': settings.MEDIA_ROOT}),
     
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)