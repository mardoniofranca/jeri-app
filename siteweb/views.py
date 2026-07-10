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
from .forms import TarefaForm
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UsuarioForm, PerfilUsuarioForm

from django.db.models import Count, Q


from django.contrib.auth import logout
from django.shortcuts import redirect


@login_required
def novo_projeto_view(request, pk=None):
    if pk:
        projeto = get_object_or_404(Projeto, pk=pk)
        titulo_pagina = "Editar Projeto"
    else:
        projeto = None
        titulo_pagina = "Novo Projeto"

    if request.method == 'POST':
        form = ProjetoForm(request.POST, instance=projeto)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, 'Projeto atualizado com sucesso!')
            else:
                messages.success(request, 'Projeto cadastrado com sucesso!')
            return redirect('menu')
    else:
        form = ProjetoForm(instance=projeto)

    context = {
        'form': form,
        'titulo_pagina': titulo_pagina,
        'projeto': projeto,
    }
    return render(request, 'novo_projeto.html', context)

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


@login_required
def nova_tarefa_view(request, pk=None):
    if pk:
        tarefa = get_object_or_404(Tarefa, pk=pk)
        titulo_pagina = "Editar Tarefa"
    else:
        tarefa = None
        titulo_pagina = "Nova Tarefa"

    if request.method == 'POST':
        form = TarefaForm(request.POST, instance=tarefa)
        if form.is_valid():
            form.save()
            if pk:
                messages.success(request, 'Tarefa atualizada com sucesso!')
            else:
                messages.success(request, 'Tarefa cadastrada com sucesso!')

            # 🔑 aqui é o pulo do gato
            projeto_id = request.POST.get('projeto_origem')
            if projeto_id:
                return redirect('detalhe_projeto', pk=projeto_id)
            return redirect('menu')
    else:
        form = TarefaForm(instance=tarefa)
        projeto_id = request.GET.get('projeto')
        if projeto_id and not pk:
            projeto = get_object_or_404(Projeto, pk=projeto_id)
            form.fields['cod_projeto'].initial = projeto.id

    context = {
        'form': form,
        'titulo_pagina': titulo_pagina,
        'tarefa': tarefa,
        'projeto_origem': request.GET.get('projeto'),
    }
    return render(request, 'nova_tarefa.html', context)

@login_required
def novo_usuario_view(request, pk=None):
    if pk:
        usuario = get_object_or_404(User, pk=pk)
        perfil = usuario.perfil  # já existe, criado pelo signal
        titulo_pagina = "Editar Usuário"
    else:
        usuario = None
        perfil = None
        titulo_pagina = "Novo Usuário"

    if request.method == 'POST':
        user_form = UsuarioForm(request.POST, instance=usuario)
        perfil_form = PerfilUsuarioForm(request.POST, instance=perfil)

        # Na criação, senha é obrigatória
        senha = request.POST.get('password')
        if not pk and not senha:
            user_form.add_error('password', 'A senha é obrigatória para novos usuários.')

        if user_form.is_valid() and perfil_form.is_valid():
            novo = user_form.save(commit=False)

            if senha:
                novo.set_password(senha)

            novo.save()  # se for criação, o signal cria o Perfil_Usuario automaticamente

            # associa e salva o perfil (criado agora ou já existente)
            perfil_obj = perfil_form.save(commit=False)
            perfil_obj.usuario = novo
            perfil_obj.save()

            if pk:
                messages.success(request, 'Usuário atualizado com sucesso!')
            else:
                messages.success(request, 'Usuário cadastrado com sucesso!')
            return redirect('menu')
    else:
        user_form = UsuarioForm(instance=usuario)
        perfil_form = PerfilUsuarioForm(instance=perfil)

    context = {
        'user_form': user_form,
        'perfil_form': perfil_form,
        'titulo_pagina': titulo_pagina,
        'usuario': usuario,
    }
    return render(request, 'novo_usuario.html', context)


@login_required
def detalhe_projeto_view(request, pk):


    projeto = get_object_or_404(Projeto, pk=pk)

    tarefas = Tarefa.objects.filter(cod_projeto=projeto).order_by('-id')

    status_tarefa = Tarefa.STATUS_TAREFA

    # --- Métricas de tarefas DESSE projeto ---
    total_tarefas = tarefas.count()
    tarefa_planejamento = tarefas.filter(status_tarefa='1').count()
    tarefa_aguardando   = tarefas.filter(status_tarefa='2').count()
    tarefa_execucao     = tarefas.filter(status_tarefa='3').count()
    tarefa_concluido    = tarefas.filter(status_tarefa='4').count()
    tarefa_bloqueado    = tarefas.filter(status_tarefa='5').count()

    # --- Usuários (time) que atuam nesse projeto (via tarefas) ---
    usuarios_ids = tarefas.exclude(usuario__isnull=True).values_list('usuario_id', flat=True).distinct()

    usuarios = User.objects.filter(id__in=usuarios_ids).annotate(
        total_tarefas_projeto=Count('tarefas', filter=Q(tarefas__cod_projeto=projeto), distinct=True)
    )

    context = {
        'projeto': projeto,
        'tarefas': tarefas,
        'usuarios': usuarios,
        'status_tarefa': status_tarefa,
        'total_tarefas': total_tarefas,
        'tarefa_planejamento': tarefa_planejamento,
        'tarefa_aguardando': tarefa_aguardando,
        'tarefa_execucao': tarefa_execucao,
        'tarefa_concluido': tarefa_concluido,
        'tarefa_bloqueado': tarefa_bloqueado,
    }

    return render(request, 'detalhe_projeto.html', context)



@login_required
def _minhas_tarefas_view(request):
    tarefas = Tarefa.objects.filter(usuario=request.user).select_related('cod_projeto').order_by('-data_final')

    # Agrupa as tarefas por status, na ordem da esteira
    colunas = []
    for valor, label in Tarefa.STATUS_TAREFA:
        colunas.append({
            'valor': valor,
            'label': label,
            'tarefas': tarefas.filter(status_tarefa=valor),
        })

    context = {
        'colunas': colunas,
        'total_tarefas': tarefas.count(),
    }
    return render(request, 'minhas_tarefas.html', context)


@login_required
def minhas_tarefas_view(request):
    projeto_id = request.GET.get('projeto')

    tarefas_usuario = Tarefa.objects.filter(usuario=request.user).select_related('cod_projeto')

    # Lista de projetos que o usuário tem tarefas, para popular o filtro (select)
    projetos_usuario = Projeto.objects.filter(
        id__in=tarefas_usuario.values_list('cod_projeto_id', flat=True).distinct()
    ).order_by('titulo')

    if projeto_id:
        # --- MODO: projeto selecionado -> só as fases desse projeto ---
        projeto_selecionado = get_object_or_404(Projeto, pk=projeto_id)
        tarefas = tarefas_usuario.filter(cod_projeto=projeto_selecionado).order_by('-data_final')

        colunas = []
        for valor, label in Tarefa.STATUS_TAREFA:
            colunas.append({
                'valor': valor,
                'label': label,
                'tarefas': tarefas.filter(status_tarefa=valor),
            })

        grupos = [{
            'projeto': projeto_selecionado,
            'colunas': colunas,
            'total': tarefas.count(),
        }]

        context = {
            'grupos': grupos,
            'projetos_usuario': projetos_usuario,
            'projeto_selecionado': projeto_selecionado,
            'total_tarefas': tarefas.count(),
        }

    else:
        # --- MODO: nenhum projeto selecionado -> agrupa por projeto, cada um com suas fases ---
        grupos = []

        for projeto in projetos_usuario:
            tarefas_projeto = tarefas_usuario.filter(cod_projeto=projeto).order_by('-data_final')

            colunas = []
            for valor, label in Tarefa.STATUS_TAREFA:
                colunas.append({
                    'valor': valor,
                    'label': label,
                    'tarefas': tarefas_projeto.filter(status_tarefa=valor),
                })

            grupos.append({
                'projeto': projeto,
                'colunas': colunas,
                'total': tarefas_projeto.count(),
            })

        # Tarefas sem projeto vinculado (cod_projeto=null), se houver
        tarefas_sem_projeto = tarefas_usuario.filter(cod_projeto__isnull=True).order_by('-data_final')
        if tarefas_sem_projeto.exists():
            colunas = []
            for valor, label in Tarefa.STATUS_TAREFA:
                colunas.append({
                    'valor': valor,
                    'label': label,
                    'tarefas': tarefas_sem_projeto.filter(status_tarefa=valor),
                })
            grupos.append({
                'projeto': None,
                'colunas': colunas,
                'total': tarefas_sem_projeto.count(),
            })

        context = {
            'grupos': grupos,
            'projetos_usuario': projetos_usuario,
            'projeto_selecionado': None,
            'total_tarefas': tarefas_usuario.count(),
        }

    return render(request, 'minhas_tarefas.html', context)

def logout_view(request):
    logout(request)
    return redirect('login')

