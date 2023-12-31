from datetime import datetime
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages,auth
from django.contrib.messages import constants
from .models import Pacientes, DadosPaciente, Refeicao, Opcao
from django.views.decorators.csrf import csrf_exempt


# xhtml2pdf
from django.template.loader import get_template
from xhtml2pdf import pisa



@login_required(login_url='/auth/login/')
def pacientes(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri = request.user)
        return render(request, 'pacientes.html', {'pacientes': pacientes})
    
    elif request.method == "POST":
        nome = request.POST.get('nome')
        sexo = request.POST.get('sexo')
        idade = request.POST.get('idade')
        email = request.POST.get('email')
        telefone = request.POST.get('telefone')


        if (len(nome.strip()) == 0) or (len(sexo.strip()) == 0) or (len(idade.strip()) == 0) or (len(email.strip()) == 0) or (len(telefone.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect('/pacientes/')

        if not idade.isnumeric():
            messages.add_message(request, constants.ERROR, 'Digite uma idade válida')
            return redirect('/pacientes/')

        pacientes = Pacientes.objects.filter(email=email)

        if pacientes.exists():
            messages.add_message(request, constants.ERROR, 'Já existe um paciente com esse E-mail')
            return redirect('/pacientes/')
        
        try:
            paciente = Pacientes(nome=nome,
                                sexo=sexo,
                                idade=idade,
                                email=email,
                                telefone=telefone, #request.user pega já o usuarioq ue está logado para cadastrar
                                nutri=request.user)

            paciente.save()

            messages.add_message(request, constants.SUCCESS, 'Paciente cadastrado com sucesso')
            return redirect('/pacientes/')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/pacientes/')
                


@login_required(login_url='/auth/login/')
def dados_paciente_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'dadospaciente.html', {'pacientes': pacientes})
    
@login_required(login_url='/auth/logar/')
def dados_paciente(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/paciente/')
        
    if request.method == "GET":
        dados_paciente = DadosPaciente.objects.filter(paciente=paciente)
        return render(request, 'paciente.html', {'paciente': paciente, 'dados_paciente': dados_paciente})
        
    elif request.method == "POST":
        peso = request.POST.get('peso')
        altura = request.POST.get('altura')
        gordura = request.POST.get('gordura')
        musculo = request.POST.get('musculo')

        hdl = request.POST.get('hdl')
        ldl = request.POST.get('ldl')
        colesterol_total = request.POST.get('ctotal')
        triglicerídios = request.POST.get('triglicerídios')
        
        paciente = DadosPaciente(paciente=paciente,
                             data=datetime.now(),
                             peso=peso,
                             altura=altura,
                             percentual_gordura=gordura,
                             percentual_musculo=musculo,
                             colesterol_hdl=hdl,
                             colesterol_ldl=ldl,
                             colesterol_total=colesterol_total,
                             trigliceridios=triglicerídios)

        paciente.save()

        messages.add_message(request, constants.SUCCESS, 'Dados cadastrados com sucesso')


        return redirect(f'/paciente/{id}')
 
 
 
    
@login_required(login_url='/auth/login/')
@csrf_exempt  #isenta a csrf token da requisição
def grafico_peso(request, id):
    paciente = Pacientes.objects.get(id=id)
    dados = DadosPaciente.objects.filter(paciente=paciente).order_by("data")
    
    pesos = [dado.peso for dado in dados]
    labels = list(range(len(pesos)))
    data = {'peso': pesos,
            'labels': labels}
    return JsonResponse(data)


def logout(request):
    auth.logout(request)
    return redirect('/auth/login')

def plano_alimentar_listar(request):
    if request.method == "GET":
        pacientes = Pacientes.objects.filter(nutri=request.user)
        return render(request, 'planoalimentar.html', {'pacientes': pacientes})
    
def plano_alimentar(request, id):
    paciente = get_object_or_404(Pacientes, id=id)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar/')

    if request.method == "GET":
        re = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        opcao = Opcao.objects.all()
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao':re, 'opcao':opcao})
    


def refeicao(request, id_paciente):
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/dadospaciente/')
    
    if request.method == "GET":
        r1 = Refeicao.objects.filter(paciente=paciente).order_by('horario')
        return render(request, 'plano_alimentar.html', {'paciente': paciente, 'refeicao':r1})

    elif request.method == "POST":
        titulo = request.POST.get('titulo')
        horario = request.POST.get('horario')
        carboidratos = request.POST.get('carboidratos')
        proteinas = request.POST.get('proteinas')
        gorduras = request.POST.get('gorduras')
        
        if (len(titulo.strip()) == 0) or (len(horario.strip()) == 0) or (len(carboidratos.strip()) == 0) or (len(proteinas.strip()) == 0) or (len(gorduras.strip()) == 0):
            messages.add_message(request, constants.ERROR, 'Preencha todos os campos')
            return redirect(f'/plano_alimentar/{id_paciente}')

        if not carboidratos.isnumeric() or not proteinas.isnumeric() or not gorduras.isnumeric():
            messages.add_message(request, constants.ERROR, 'numeros inválidos')
            return redirect(f'/plano_alimentar/{id_paciente}')

        r1 = Refeicao(paciente=paciente,
                      titulo=titulo,
                      horario=horario,
                      carboidratos=carboidratos,
                      proteinas=proteinas,
                      gorduras=gorduras)

        r1.save()

        messages.add_message(request, constants.SUCCESS, 'Refeição cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')
    
def opcao(request, id_paciente):
    if request.method == "POST":
        id_refeicao = request.POST.get('refeicao')
        imagem = request.FILES.get('imagem')
        descricao = request.POST.get("descricao")

        o1 = Opcao(refeicao_id=id_refeicao,
                   imagem=imagem,
                   descricao=descricao)

        o1.save()

        messages.add_message(request, constants.SUCCESS, 'Opcao cadastrada')
        return redirect(f'/plano_alimentar/{id_paciente}')
    
    

def pdf(request, id_paciente):
    
    paciente = get_object_or_404(Pacientes, id=id_paciente)
    if not paciente.nutri == request.user:
        messages.add_message(request, constants.ERROR, 'Esse paciente não é seu')
        return redirect('/plano_alimentar_listar/')
    
    
    re = Refeicao.objects.filter(paciente=paciente).order_by('horario')
    opcao = Opcao.objects.all()
        
    template_path = 'pdf_template.html'
    
    context = {
        'paciente': paciente,
        'refeicao':re,
        'opcao':opcao,
             
               }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    #1 - cria pdf e faz download:
    response['Content-Disposition'] = f'attachment; filename="Dieta_{paciente}.pdf"'

    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
       html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
       return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response