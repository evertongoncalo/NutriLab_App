from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from .utils import *
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages,auth
from django.conf import settings
import os
from .models import Ativacao
from hashlib import sha256


def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    
    elif request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not password_is_valid(request, senha,confirmar_senha):
            return redirect('/auth/register')
        try:
            user = User.objects.create_user(username=usuario,email=email,password=senha,is_active=False) #is active é para o usuario receber o email pra confirmar e depois ai sim poder acessar o sistema.
            print(user)
            user.save()
            
            token = sha256(f"{usuario}+{email}".encode()).hexdigest() #token criaod com a hashlib
            ativacao = Ativacao(token=token,user=user)
            ativacao.save()
            
            path_template = os.path.join(settings.BASE_DIR, 'templates/emails/cad_confirmado.html')
            email_html(path_template, 'Cadastro confirmado', [email,], username=usuario,link_ativacao=f"127.0.0.1:8000/auth/ativar_conta/{token}")
            messages.add_message(request,constants.SUCCESS, "Usuario cadastrado")
            
            
            return redirect('/auth/login')
        except:
            messages.add_message(request,constants.ERROR, "Erro do sistema")
            return redirect('/auth/register')
        
        
def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/')
        return render(request, 'login.html')

    elif request.method == "POST":
        username = request.POST.get('usuario')
        senha = request.POST.get('senha')

        usuario = auth.authenticate(username=username, password=senha)

        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválidos')
            return redirect('/auth/login')
        else:
            auth.login(request, usuario)
            return redirect('/pacientes')
            
    

def login(request):
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')

def sair(request):
    auth.logout(request)
    return redirect('/auth/login')

def ativar_conta(request, token):
    token = get_object_or_404(Ativacao, token=token) #retorna o obejto do banco de dados ou retorna 404
    if token.ativo:
        messages.add_message(request, constants.WARNING, 'Essa token já foi usado')
        return redirect('/auth/logar')
    user = User.objects.get(username=token.user.username)
    user.is_active = True
    user.save()
    token.ativo = True
    token.save()
    messages.add_message(request, constants.SUCCESS, 'Conta ativa com sucesso')
    return redirect('/auth/login')

