from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FormCliente, FormAtendimento
from .models import Cliente, Atendimento, Movimentacao, Projeto, Tarefa, Cliente_Hist
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/menu')
        else:
            messages.error(request, 'Usuário ou senha inválidos')
    return render(request, 'login.html')


def pct(valor, total):
    return round((valor / total) * 100, 1) if total else 0


@login_required
def menu_view(request):
    hoje = timezone.now().date()
    projetos = Projeto.objects.all().order_by('-id')
    tarefas  = Tarefa.objects.all().order_by('-id')


    status_choices = Projeto.STATUS_PROJETO
    status_tarefa  = Tarefa.STATUS_TAREFA

    total = projetos.count()
    negociacao = projetos.filter(status_projeto='1').count()
    aguardando = projetos.filter(status_projeto='2').count()
    execucao = projetos.filter(status_projeto='3').count()
    concluido = projetos.filter(status_projeto='4').count()
    bloqueado = projetos.filter(status_projeto='5').count()

    context = {
        'hoje': hoje,
        'projetos': projetos,
        'tarefas' : tarefas,
        'total_projetos': total,
        "pct_negociacao": pct(negociacao, total),
        "pct_aguardando": pct(aguardando, total),
        "pct_execucao": pct(execucao, total),
        "pct_concluido": pct(concluido, total),
        "pct_bloqueado": pct(bloqueado, total),
        "negociacao": negociacao,
        "aguardando": aguardando,
        "execucao": execucao,
        "concluido": concluido,
        "bloqueado": bloqueado,
        "status_choices": status_choices,
        "status_tarefa": status_tarefa,
    }

    return render(request, 'menu.html', context)


@login_required
def cliente_view(request):
    return render(request, 'cliente.html')


@login_required
def atendimento_view(request):
    return render(request, 'atendimento.html')