from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required



from django.shortcuts import render, get_object_or_404, redirect
from .forms import FormCliente, FormAtendimento
from .models import Cliente, Atendimento, Movimentacao, Projeto
from django.http import HttpResponse
from .models import Cliente_Hist
from django.core.paginator import Paginator

from django.db.models import Count
from django.utils import timezone
from datetime import timedelta

from django.db.models import Count

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            login(request, user)

            return redirect('/menu')

        else:

            messages.error(
                request,
                'Usuário ou senha inválidos'
            )
    return render(request, 'login.html')



@login_required
def menu_view(request):   

    total = Projeto.objects.count()

    negociacao = Projeto.objects.filter(status_projeto='1').count()
    aguardando = Projeto.objects.filter(status_projeto='2').count()
    execucao = Projeto.objects.filter(status_projeto='3').count()
    concluido = Projeto.objects.filter(status_projeto='4').count()
    bloqueado = Projeto.objects.filter(status_projeto='5').count()



    def pct(valor):
        return round((valor / total) * 100, 1) if total else 0
        hoje = timezone.now().date()
        projetos = Projeto.objects.all().order_by('-id')
        status_choices = Projeto.STATUS_PROJETO  

    context = {
        'hoje': hoje,
        'projetos': projetos,
        'total_projetos': projetos.count(),
        "total_projetos": total,
        "pct_negociacao": pct(negociacao),
        "pct_aguardando": pct(aguardando),
        "pct_execucao": pct(execucao),
        "pct_concluido": pct(concluido),
        "pct_bloqueado": pct(bloqueado),

        "negociacao": negociacao,
        "aguardando": aguardando,
        "execucao": execucao,
        "concluido": concluido,
        "bloqueado": bloqueado,
        "status_choices": status_choices,

    }

    return render(request, 'menu.html', context)



@login_required
def cliente_view(request):
    return render(request, 'cliente.html')


@login_required
def atendimento_view(request):
    return render(request, 'atendimento.html')