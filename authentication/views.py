from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *
from django.contrib.auth.models import User
from django.contrib.messages import constants
from django.contrib import messages,auth



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
            return redirect('/')    

def login(request):
    return render(request, 'login.html')

def sair(request):
    auth.logout(request)
    return redirect('/auth/login')