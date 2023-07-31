from django.shortcuts import render, redirect
from django.http import HttpResponse
from .utils import *



def register(request):
    if request.method == 'POST':
        usuario = request.POST.get('usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        if not password_is_valid(request, senha,confirmar_senha):
            return redirect('/auth/register')
        
    elif request.method == 'GET':
        return render(request, 'register.html')

def login(request):
    return render(request, 'login.html')