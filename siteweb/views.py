from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Projeto, Tarefa
from django.contrib.auth.models import User

from django.http import HttpResponse
from django.core.paginator import Paginator
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import render, redirect
from .forms import ProjetoForm

@login_required
def novo_projeto_view(request):
    if request.method == 'POST':
        form = ProjetoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Projeto cadastrado com sucesso!')
            return redirect('menu')  # ajuste para o nome da sua url de listagem
    else:
        form = ProjetoForm()

    return render(request, 'novo_projeto.html', {'form': form})

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

    usuarios = User.objects.annotate(
        total_projetos=Count('projetos', distinct=True),
        total_tarefas=Count('tarefas', distinct=True)
    ).order_by('username')

    status_choices = Projeto.STATUS_PROJETO
    status_tarefa  = Tarefa.STATUS_TAREFA

    # --- Métricas de PROJETOS ---
    total = projetos.count()
    negociacao = projetos.filter(status_projeto='1').count()
    aguardando = projetos.filter(status_projeto='2').count()
    execucao = projetos.filter(status_projeto='3').count()
    concluido = projetos.filter(status_projeto='4').count()
    bloqueado = projetos.filter(status_projeto='5').count()

    # --- Métricas de TAREFAS ---
    total_tarefas = tarefas.count()
    tarefa_planejamento = tarefas.filter(status_tarefa='1').count()
    tarefa_aguardando   = tarefas.filter(status_tarefa='2').count()
    tarefa_execucao     = tarefas.filter(status_tarefa='3').count()
    tarefa_concluido    = tarefas.filter(status_tarefa='4').count()
    tarefa_bloqueado    = tarefas.filter(status_tarefa='5').count()

    # --- Métricas de usuários ---
    total_usuarios = usuarios.count()
    usuarios_ativos = usuarios.filter(is_active=True).count()
    usuarios_com_projetos = usuarios.filter(total_projetos__gt=0).count()
    usuarios_sem_projetos = total_usuarios - usuarios_com_projetos
    usuarios_com_tarefas = usuarios.filter(total_tarefas__gt=0).count()
    usuarios_sem_tarefas = total_usuarios - usuarios_com_tarefas

    media_projetos_usuario = round(total / total_usuarios, 1) if total_usuarios else 0
    media_tarefas_usuario = round(total_tarefas / total_usuarios, 1) if total_usuarios else 0

    context = {
        'hoje': hoje,
        'projetos': projetos,
        'tarefas' : tarefas,
        'usuarios': usuarios,
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

        # métricas de tarefas
        "total_tarefas": total_tarefas,
        "pct_tarefa_planejamento": pct(tarefa_planejamento, total_tarefas),
        "pct_tarefa_aguardando": pct(tarefa_aguardando, total_tarefas),
        "pct_tarefa_execucao": pct(tarefa_execucao, total_tarefas),
        "pct_tarefa_concluido": pct(tarefa_concluido, total_tarefas),
        "pct_tarefa_bloqueado": pct(tarefa_bloqueado, total_tarefas),
        "tarefa_planejamento": tarefa_planejamento,
        "tarefa_aguardando": tarefa_aguardando,
        "tarefa_execucao": tarefa_execucao,
        "tarefa_concluido": tarefa_concluido,
        "tarefa_bloqueado": tarefa_bloqueado,

        # métricas de usuários
        "total_usuarios": total_usuarios,
        "usuarios_ativos": usuarios_ativos,
        "usuarios_com_projetos": usuarios_com_projetos,
        "usuarios_sem_projetos": usuarios_sem_projetos,
        "usuarios_com_tarefas": usuarios_com_tarefas,
        "usuarios_sem_tarefas": usuarios_sem_tarefas,
        "media_projetos_usuario": media_projetos_usuario,
        "media_tarefas_usuario": media_tarefas_usuario,
    }

    return render(request, 'menu.html', context)

    hoje = timezone.now().date()
    projetos = Projeto.objects.all().order_by('-id')
    tarefas  = Tarefa.objects.all().order_by('-id')

    usuarios = User.objects.annotate(
        total_projetos=Count('projetos', distinct=True),
        total_tarefas=Count('tarefas', distinct=True)
    ).order_by('username')

    status_choices = Projeto.STATUS_PROJETO
    status_tarefa  = Tarefa.STATUS_TAREFA

    total = projetos.count()
    negociacao = projetos.filter(status_projeto='1').count()
    aguardando = projetos.filter(status_projeto='2').count()
    execucao = projetos.filter(status_projeto='3').count()
    concluido = projetos.filter(status_projeto='4').count()
    bloqueado = projetos.filter(status_projeto='5').count()

    # --- Métricas de usuários ---
    total_usuarios = usuarios.count()
    usuarios_ativos = usuarios.filter(is_active=True).count()
    usuarios_com_projetos = usuarios.filter(total_projetos__gt=0).count()
    usuarios_sem_projetos = total_usuarios - usuarios_com_projetos
    usuarios_com_tarefas = usuarios.filter(total_tarefas__gt=0).count()
    usuarios_sem_tarefas = total_usuarios - usuarios_com_tarefas

    media_projetos_usuario = round(total / total_usuarios, 1) if total_usuarios else 0
    media_tarefas_usuario = round(tarefas.count() / total_usuarios, 1) if total_usuarios else 0

    context = {
        'hoje': hoje,
        'projetos': projetos,
        'tarefas' : tarefas,
        'usuarios': usuarios,
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

        # métricas de usuários
        "total_usuarios": total_usuarios,
        "usuarios_ativos": usuarios_ativos,
        "usuarios_com_projetos": usuarios_com_projetos,
        "usuarios_sem_projetos": usuarios_sem_projetos,
        "usuarios_com_tarefas": usuarios_com_tarefas,
        "usuarios_sem_tarefas": usuarios_sem_tarefas,
        "media_projetos_usuario": media_projetos_usuario,
        "media_tarefas_usuario": media_tarefas_usuario,
    }

    return render(request, 'menu.html', context)

